from datetime import datetime
from pennyutils.domain.handlers.budget_handler import get_user_budgets

def run(aws_payload):
    print(f'{datetime.now()} Starting AWS lambda function')
    print(f'{datetime.now()} Body event: {aws_payload}')
    try:
        parameters = aws_payload.get("pathParameters") or {}
        if 'id_user' not in parameters:
            raise ValueError("Campo obrigatório ausente: id_user")

        try:
            id_user = int(parameters['id_user'])
        except (TypeError, ValueError):
            raise ValueError("id_user inválido: deve ser um número inteiro.")
        if id_user <= 0:
            raise ValueError("id_user inválido: deve ser um número inteiro positivo.")

        response = get_user_budgets(id_user)

        print(f'Request OK: Response {response}')
        return response

    except Exception as e:
        print(f'Request Failed: Response {e}')
        raise ValueError(f"Ocorreu um erro inesperado: {e}")
