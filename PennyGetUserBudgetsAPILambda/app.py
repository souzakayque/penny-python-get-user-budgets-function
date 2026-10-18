from domain.dto.response_data import ResponseData
from business.get_user_budgets import run
from pennyutils.core.auth.validator import validate

def lambda_handler(event, context):
    try:
        if not validate(event):
            response = ResponseData(message="Unauthorized", status_code=401)
            return response.json

        result_handler = run(event)

        response = ResponseData(response=result_handler)
        return response.json

    except Exception as e:
        response = ResponseData(message=str(e), status_code=400)
        return response.json
