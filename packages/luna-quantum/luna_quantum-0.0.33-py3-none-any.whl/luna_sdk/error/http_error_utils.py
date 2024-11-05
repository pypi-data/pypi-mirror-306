import logging
from typing import Optional

import httpx
from httpx import RequestError, Response

from luna_sdk.exceptions.luna_server_exception import LunaServerException
from luna_sdk.schemas.error_message import ErrorMessage


class HttpErrorUtils:
    @staticmethod
    def __sdk_custom_request_errors(
        response: Response,
    ) -> Optional[LunaServerException]:
        """
        Check if the response needs a custom error message from the SDK.

        This is the place to add other custom error messages.
        This is helpful then the default http error messages are not enough for the user.

        Parameters
        ----------
        response:
            Response object from the request

        Returns
        -------
        Optional[LunaServerException]
            If the response needs a custom error message, return the exception.
            Otherwise, return None.
        """
        exception: Optional[LunaServerException] = None

        def create_error_message(
            internal_code: str, message: str
        ) -> LunaServerException:
            return LunaServerException(
                response.status_code,
                ErrorMessage(
                    internal_code=f"SDK-{internal_code}",
                    message=message,
                ),
            )

        if response.status_code == 502:
            # Catch error when upload was too long
            exception = create_error_message(
                "LUNA_GATEWAY_TIMEOUT",
                "The Luna server did not respond within time,"
                " leading to a timeout. Try reducing the size of the optimization.",
            )

        elif response.status_code == 403:
            exception = create_error_message(
                "FORBIDDEN",
                response.text,
            )

        return exception

    @staticmethod
    def check_for_error(response: Response) -> None:
        """
        Check if an error occurred and rais the error if so.

        Parameters
        ----------
        response: Response
            Response object from the request

        Raises
        ------
        LunaServerException
            If an error occurred with the request. The error message is in the exception.
        RequestError
            If an error occurred with the request outside the http status codes 4xx and 5xx.
        """
        try:
            response.read()
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            exception: Optional[LunaServerException]

            try:
                error_msg: ErrorMessage = ErrorMessage.model_validate_json(
                    response.text
                )
                # Convert the error message to the correct exception
                exception = LunaServerException(response.status_code, error_msg)

            except ValueError:
                # The server can generate errors that are in a different format, and we
                # have less to no control how they look like.
                # In this case, we will try to create a custom error messages.
                exception = HttpErrorUtils.__sdk_custom_request_errors(response)

            if exception:
                logging.error(exception, exc_info=False)
                raise exception
            else:
                logging.error(exception, exc_info=True)
                raise e

        except RequestError as e:
            logging.error(e, exc_info=True)
            raise e
