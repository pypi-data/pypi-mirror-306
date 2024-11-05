from typing import Optional

from luna_sdk.controllers.luna_platform_client import LunaPlatformClient, LunaPrefixEnum
from luna_sdk.interfaces.clients.luna_transform_i import ILunaTransform
from luna_sdk.interfaces.cplex_repo_i import ICplexRepo
from luna_sdk.interfaces.lp_repo_i import ILPRepo
from luna_sdk.repositories.cplex_repo import CplexRepo
from luna_sdk.repositories.lp_repo import LPRepo


class LunaTransform(LunaPlatformClient, ILunaTransform):
    cplex: ICplexRepo = None  # type: ignore
    lp: ILPRepo = None  # type: ignore

    def __init__(
        self,
        api_key: str,
        timeout: Optional[float] = 240.0,
    ):
        """
        LunaTransform is the main entrypoint for all LunaTransform related tasks.

        Parameters
        ----------
        api_key: str
            User's API key
        timeout: float
            Default timeout in seconds for the requests via the LunaQ client. `None`
            means that the SDK uses no timeouts. Note that either way the Luna platform
            itself will time out after 240 seconds.
            Default: 240.0
        """
        super().__init__(
            api_key=api_key,
            api=LunaPrefixEnum.LUNA_SOLVE,
            timeout=timeout,
        )

        self.cplex = CplexRepo(self._client)
        self.lp = LPRepo(self._client)
