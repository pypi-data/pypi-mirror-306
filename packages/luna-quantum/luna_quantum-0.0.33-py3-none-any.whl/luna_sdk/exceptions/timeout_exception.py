from luna_sdk.exceptions.luna_exception import LunaException


class TimeoutException(LunaException):
    def __init__(self):
        super().__init__(
            "Luna Timeout. The request took too long to complete."
            " Please increase timeout value or try again later."
            " If the problem persists, please contact our support team."
        )
