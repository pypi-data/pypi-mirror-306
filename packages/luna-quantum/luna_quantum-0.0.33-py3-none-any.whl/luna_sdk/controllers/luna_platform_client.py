import os
from enum import Enum
from typing import Optional, Literal

import httpx

from luna_sdk.controllers.luna_http_client import LunaHTTPClient
from luna_sdk.error.http_error_utils import HttpErrorUtils
from luna_sdk.interfaces.clients.client_i import IClient


class LunaPrefixEnum(str, Enum):
    LUNA_SOLVE = "luna-solve"
    LUNA_Q = "luna-q"


def check_httpx_exceptions(response):
    HttpErrorUtils.check_for_error(response)


class APIKeyAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Luna-API-Key"] = self.token
        yield request


class LunaPlatformClient(IClient):
    _base_url: str = ""

    _client: httpx.Client = None  # type: ignore

    def __init__(
        self,
        api_key: str,
        api: LunaPrefixEnum,
        base_url: str = os.getenv("LUNA_BASE_URL", "https://api.aqarios.com"),
        timeout: Optional[float] = 240.0,
    ):
        """
        LunaPlatformClient is a main entrypoint of the SDK.
        All the operations with entities should be processed using an instance of
        LunaPlatformClient.

        Parameters
        ----------
        api_key:
            User's API key
        api: str
            Current API with which luna client is working. Can be luna-solve or luna-q.
        base_url:
            Base API URL.
            If you want to use API not on your local PC then change it.
            You can do that by setting the environment variable LUNA_BASE_URL.
            Default value https://api.aqarios.com.
        timeout:
            Default timeout in seconds for the requests via the LunaQ client. `None`
            means that the SDK uses no timeouts. Note that either way the Luna platform
            itself will time out after 240 seconds.
            Default: 240.0
        """
        self._base_url = f"{base_url}/{api.value}/api/v1"

        # setup client
        self._client = LunaHTTPClient(
            auth=APIKeyAuth(api_key),
            base_url=self._base_url,
            follow_redirects=True,
            timeout=timeout,
            event_hooks={"response": [check_httpx_exceptions]},
        )

    def __del__(self):
        if hasattr(self, "_client"):
            try:
                self._client.close()
            except Exception:
                pass  # doesn't seem to be a big deal, so just ignore
