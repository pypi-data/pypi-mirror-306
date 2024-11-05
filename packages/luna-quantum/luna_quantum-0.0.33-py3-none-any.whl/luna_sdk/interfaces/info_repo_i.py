from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas.solver_info import SolverInfo


class IInfoRepo(IRepository, ABC):
    @abstractmethod
    def solvers_available(
        self, solver_name: Optional[str] = None, **kwargs
    ) -> Dict[str, Dict[str, SolverInfo]]:
        """
        Get list of available solvers.

        Parameters
        ----------
        solver_name: Optional[str]
            Name of the solver that should be retrieved. If not specified, all solvers
            will be returned.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Dict[str, Dict[str, SolverInfo]]
            Dictionary containing the provider name as the key, and a dictionary of
            the solver name and solver-specific information as the value.
        """
        raise NotImplementedError

    @abstractmethod
    def providers_available(self, **kwargs) -> List[str]:
        """
        Get list of available providers.

        Parameters
        ----------
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        List[str]
            List of available QPU providers.
        """
        raise NotImplementedError
