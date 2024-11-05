from typing import Optional

from luna_sdk.controllers.luna_platform_client import LunaPlatformClient, LunaPrefixEnum
from luna_sdk.interfaces import ICircuitRepo
from luna_sdk.interfaces.clients.luna_q_i import ILunaQ
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.repositories import CircuitRepo, QpuTokenRepo


class LunaQ(LunaPlatformClient, ILunaQ):
    qpu_token: IQpuTokenRepo = None  # type: ignore
    circuit: ICircuitRepo = None  # type: ignore

    def __init__(self, api_key: str, timeout: Optional[float] = 240.0):
        """
        LunaQ is the main entrypoint for all LunaQ related tasks.

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
        super().__init__(api_key=api_key, api=LunaPrefixEnum.LUNA_Q, timeout=timeout)

        self.circuit = CircuitRepo(self._client)
        self.qpu_token = QpuTokenRepo(self._client)
