from importlib.metadata import version

import httpx
from httpx import Client, Response

from luna_sdk.error.http_error_utils import HttpErrorUtils
from luna_sdk.exceptions.timeout_exception import TimeoutException


class LunaHTTPClient(Client):
    _version: str = version("luna-quantum")

    _user_agent: str = f"LunaSDK/{_version}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers["User-Agent"] = self._user_agent

    def request(self, *args, **kwargs) -> Response:
        try:
            response: Response = super().request(*args, **kwargs)
        except httpx.TimeoutException:
            # Handle all possible in httpx timeout exceptions
            raise TimeoutException()
        HttpErrorUtils.check_for_error(response)
        return response
