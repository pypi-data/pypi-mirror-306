from luna_sdk.exceptions.luna_exception import LunaException
from luna_sdk.schemas.error_message import ErrorMessage


class LunaServerException(LunaException):
    http_status_code: int
    error_message: ErrorMessage

    def __init__(self, http_status_code: int, error_message: ErrorMessage):
        self.http_status_code = http_status_code
        self.error_message = error_message
        super().__init__(error_message.message)

    def __str__(self):
        return (
            f"The Luna-Server reported the error '{self.error_message.internal_code}' "
            f"with the message:\n {self.error_message.message}"
        )
