import json
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def _stub(name, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


# pennyutils abre conexão com o banco no import; os testes usam stubs.
for pkg in ['pennyutils', 'pennyutils.core', 'pennyutils.core.auth',
            'pennyutils.domain', 'pennyutils.domain.handlers']:
    _stub(pkg)
_stub('pennyutils.core.auth.validator', validate=MagicMock())
_stub('pennyutils.domain.handlers.budget_handler', get_user_budgets=MagicMock())

import app  # noqa: E402
from business import get_user_budgets  # noqa: E402


def make_event(id_user=1):
    path = None if id_user is None else {'id_user': id_user}
    return {'headers': {'Authorization': 'Bearer x'}, 'pathParameters': path}


BUDGETS = [
    {'id_budget': 10, 'created_at': '2025-01-01', 'created_by': 1, 'id_user': 1,
     'de_budget': 'Mercado', 'no_budget_value': 800.0, 'id_expense_subcategory': 5,
     'de_expense_subcategory': 'Supermercado', 'id_expense_category': 2,
     'de_expense_category': 'Alimentação'},
    {'id_budget': 11, 'created_at': '2025-01-02', 'created_by': 1, 'id_user': 1,
     'de_budget': 'Lazer', 'no_budget_value': 300.0, 'id_expense_subcategory': 8,
     'de_expense_subcategory': 'Cinema', 'id_expense_category': 3,
     'de_expense_category': 'Entretenimento'},
]


class RunTests(unittest.TestCase):
    @patch.object(get_user_budgets, 'get_user_budgets', return_value=BUDGETS)
    def test_returns_multiple_budgets(self, handler):
        result = get_user_budgets.run(make_event('1'))
        self.assertEqual(result, BUDGETS)
        self.assertEqual(len(result), 2)

    @patch.object(get_user_budgets, 'get_user_budgets', return_value=[])
    def test_user_without_budgets_returns_empty_list(self, handler):
        self.assertEqual(get_user_budgets.run(make_event('1')), [])

    @patch.object(get_user_budgets, 'get_user_budgets', return_value=[])
    def test_query_uses_requested_user_id_as_int(self, handler):
        get_user_budgets.run(make_event('42'))
        handler.assert_called_once_with(42)

    @patch.object(get_user_budgets, 'get_user_budgets')
    def test_missing_id_user(self, handler):
        for event in [make_event(None), {'pathParameters': {}}, {}]:
            with self.assertRaises(ValueError) as ctx:
                get_user_budgets.run(event)
            self.assertIn('id_user', str(ctx.exception))
        handler.assert_not_called()

    @patch.object(get_user_budgets, 'get_user_budgets')
    def test_invalid_id_user(self, handler):
        for value in ['abc', '', '1.5', '0', '-3', None]:
            event = {'pathParameters': {'id_user': value}}
            with self.assertRaises(ValueError) as ctx:
                get_user_budgets.run(event)
            self.assertIn('id_user inválido', str(ctx.exception))
        handler.assert_not_called()

    @patch.object(get_user_budgets, 'get_user_budgets',
                  side_effect=Exception('O serviço de dados está temporariamente indisponível.'))
    def test_database_failure(self, handler):
        with self.assertRaises(ValueError) as ctx:
            get_user_budgets.run(make_event('1'))
        self.assertIn('temporariamente indisponível', str(ctx.exception))


class LambdaHandlerTests(unittest.TestCase):
    @patch.object(app, 'validate', return_value=True)
    @patch.object(app, 'run', return_value=BUDGETS)
    def test_success_returns_200_with_json_list(self, run, validate):
        result = app.lambda_handler(make_event('1'), None)

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers'], {'Content-Type': 'application/json'})
        body = json.loads(result['body'])
        self.assertEqual(body['response'], BUDGETS)
        self.assertEqual(body['message'], '')

    @patch.object(app, 'validate', return_value=True)
    @patch.object(app, 'run', return_value=[])
    def test_no_budgets_returns_200_with_empty_list(self, run, validate):
        result = app.lambda_handler(make_event('1'), None)

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body'])['response'], [])

    @patch.object(app, 'validate', return_value=False)
    @patch.object(app, 'run')
    def test_unauthorized_returns_401(self, run, validate):
        result = app.lambda_handler(make_event('1'), None)

        self.assertEqual(result['statusCode'], 401)
        self.assertEqual(json.loads(result['body'])['message'], 'Unauthorized')
        run.assert_not_called()

    @patch.object(app, 'validate', return_value=True)
    @patch.object(app, 'run', side_effect=ValueError('Campo obrigatório ausente: id_user'))
    def test_error_returns_400_with_message(self, run, validate):
        result = app.lambda_handler(make_event(None), None)

        self.assertEqual(result['statusCode'], 400)
        self.assertIn('id_user', json.loads(result['body'])['message'])

    @patch.object(app, 'validate', side_effect=RuntimeError('auth lambda unreachable'))
    def test_validate_exception_returns_400(self, validate):
        result = app.lambda_handler(make_event('1'), None)
        self.assertEqual(result['statusCode'], 400)


if __name__ == '__main__':
    unittest.main()
