from http import HTTPStatus
from flask import make_response, Response


class APIError:
    """API error with corresponding HTTP status code

    Attributes:
        http_status -- input attribute name that is missing or invalid
        message -- explanation of the error
    """

    def __init__(self, http_status: HTTPStatus, message: str = "API Error"):
        self.http_status = http_status
        self.message = message
    
    def get_response(self) -> Response:
        return make_response({"message": self.message}, self.http_status.value)