from typing import Any, Dict, List, Optional

from luna_sdk.interfaces.info_repo_i import IInfoRepo
from luna_sdk.schemas.solver_info import SolverInfo


class InfoRepo(IInfoRepo):
    _endpoint = "/"

    _endpoint_solvers = "/solvers"
    _endpoint_providers = "/providers"

    def solvers_available(
        self, solver_name: Optional[str] = None, **kwargs
    ) -> Dict[str, Dict[str, SolverInfo]]:
        params = {}
        if solver_name:
            params["solver_name"] = solver_name

        response = self._client.get(
            f"{self._endpoint_solvers}/available", params=params, **kwargs
        )

        response.raise_for_status()

        json: Dict[str, Dict[str, Any]] = response.json()
        to_return: Dict[str, Dict[str, SolverInfo]] = {}
        for provider in json:
            to_return[provider] = {}
            for solver in json[provider]:
                to_return[provider][solver] = SolverInfo.model_validate(
                    json[provider][solver]
                )

        return to_return

    def providers_available(self, **kwargs) -> List[str]:
        response = self._client.get(f"{self._endpoint_providers}/available", **kwargs)

        response.raise_for_status()

        return [i for i in response.json()]
