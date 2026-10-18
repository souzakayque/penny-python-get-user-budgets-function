import json

class ResponseData:
    def __init__(self, message="", response="", status_code=200):
        self._json = {}
        self._status_code = 200 if status_code is None else status_code
        self._message = message
        self._response = response
        self._set_status_code()
        self._set_json()

    @property
    def json(self):
        return self._json
    
    @json.setter
    def json (self, value):
        self._json = value

    def _set_status_code(self) -> None:
        if isinstance(self._message, ValueError) or len(self._message) > 0:
            self._statusCode = 400 

    def _set_json(self):
        self._json = {
            'statusCode': self._status_code,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': self._message,
                'response': self._response
            }, default=str)
        }
