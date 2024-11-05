from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.qpu_token import TokenProvider
from luna_sdk.schemas.solution import (
    Result,
    Solution,
    UseCaseRepresentation,
    UseCaseResult,
)


class ISolutionsRepo(IRepository, ABC):
    @abstractmethod
    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        limit: int = 50,
        offset: int = 0,
        optimization_id: Optional[str] = None,
        **kwargs,
    ) -> List[Solution]:
        """
        Get list of available optimizations.

        Parameters
        ----------
        timeframe: Optional[TimeframeEnum]
            Only return Solutions created within a specified timeframe. Default None.
        limit:
            Limit the number of Optimizations to be returned. Default value 10.
        offset:
            Offset the list of solutions by this amount. Default value 0.
        optimization_id: Optional[str]
            Show solutions for only this optimization id. Default None.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        List[SolutionOut]
            List of SolutionOut instances.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, solution_id: str, **kwargs) -> Solution:
        """
        Retrieve one optimization by id.

        Parameters
        ----------
        solution_id: str
            Id of the solution that should be retrieved.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Solution
            Solution instance
        """
        raise NotImplementedError

    @abstractmethod
    def get_use_case_representation(
        self, solution_id: str, **kwargs
    ) -> UseCaseRepresentation:
        """
        Get the use-case-specific representation of a solution.

        Parameters
        ----------
        solution_id: str
            Id of the solution that should be retrieved.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        UseCaseRepresentation
            The use-case-specific representation
        """

    @abstractmethod
    def delete(self, solution_id: str, **kwargs) -> None:
        """
        Delete one optimization by id.

        Parameters
        ----------
        solution_id: str
            Id of the optimization that should be deleted.
        **kwargs
            Parameters to pass to `httpx.request`.
        """
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        optimization_id: str,
        solver_name: str,
        provider: str,
        qpu_tokens: Optional[TokenProvider] = None,
        solver_parameters: Optional[Union[Dict[str, Any], BaseModel]] = None,
        encryption_key: Optional[str] = None,
        name: Optional[str] = None,
        fail_on_invalid_params: bool = True,
        **kwargs,
    ) -> Solution:
        """
        Create a solution for optimization.

        Parameters
        ----------
        optimization_id: str
            The id of the optimization for which solution should be created.
        solver_name: str
            The name of the solver to use.
        provider: str
            The name of the provider to use.
        qpu_tokens: Optional[TokenProvider]
            The tokens to be used for the QPU.
        solver_parameters: Optional[Union[Dict[str, Any], BaseModel]]
            Parameters to be passed to the solver.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        name: Optional[str]
            Default: None, The name of the solution to create.
        fail_on_invalid_params: bool
            Default: true. Disable the local solver parameter validation.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        SolutionOut
            The location where the solution can be found once solving is complete.
        """
        raise NotImplementedError

    @abstractmethod
    def create_blocking(
        self,
        optimization_id: str,
        solver_name: str,
        provider: str,
        qpu_tokens: Optional[TokenProvider] = None,
        solver_parameters: Optional[Union[Dict[str, Any], BaseModel]] = None,
        sleep_time_max: float = 60.0,
        sleep_time_increment: float = 5.0,
        sleep_time_initial: float = 5.0,
        encryption_key: Optional[str] = None,
        name: Optional[str] = None,
        fail_on_invalid_params: bool = True,
        **kwargs,
    ) -> Solution:
        """
        Create a solution for optimization. This method will block your code until the solution is ready.
        Depending on the problem size, this can take a long time.

        Parameters
        ----------
        optimization_id: str
            The id of the optimization for which solution should be created.
        solver_name: str
            The name of the solver to use.
        provider: str
            The name of the provider to use.
        qpu_tokens: Optional[TokenProvider] = None
            The tokens to be used for the QPU.
        solver_parameters: Optional[Union[Dict[str, Any], BaseModel]]
            Parameters to be passed to the solver.
        sleep_time_max: float
            Maximum time to sleep between requests.
        sleep_time_increment: float
            Increment of sleep time between requests. Initial sleep time will be
        sleep_time_initial: float
            Initial sleep time.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        name: Optional[str]
            Default: None, The name of the solution to create.
        fail_on_invalid_params: bool
            Default: true. Disable the local solver parameter validation.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        SolutionOut
            The location where the solution can be found once solving is complete.
        """
        raise NotImplementedError

    @abstractmethod
    def get_best_result(self, solution: Solution) -> Optional[Result]:
        """
        Retrieves the best result from a solution.

        Parameters
        ----------
        solution : Solution
            The solution received via `solutions.get` or `solutions.get_all`.

        Returns
        -------
        Optional[Result]
            The best result of the solution. If there are several best solutions with
            the same objective value, return only the first. If the solution results are
            not (yet) available or the solution sense is `None`, `None` is returned.
        """
        raise NotImplementedError

    @abstractmethod
    def get_best_use_case_result(
        self, use_case_representation: UseCaseRepresentation
    ) -> Optional[UseCaseResult]:
        """
        Retrieves the best result from a solution's use case representation.

        Parameters
        ----------
        use_case_representation : UseCaseRepresentation
            A solution's use case representation.

        Returns
        -------
        UseCaseResult | None
            The best result of the solution. If there are several best solutions with
            the same objective value, return only the first. If the solution results are
            not (yet) available or the solution sense is `None`, `None` is returned.
        """
        raise NotImplementedError
