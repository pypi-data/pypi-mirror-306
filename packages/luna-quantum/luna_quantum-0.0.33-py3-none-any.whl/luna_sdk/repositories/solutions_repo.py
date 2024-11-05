import logging
import os
from time import sleep
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, ValidationError

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.solutions_repo_i import ISolutionsRepo
from luna_sdk.schemas.create.solution import SolutionIn
from luna_sdk.schemas.enums.solution import SenseEnum
from luna_sdk.schemas.enums.status import StatusEnum
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.qpu_token import TokenProvider
from luna_sdk.schemas.rest.qpu_token.token_provider import RestAPITokenProvider
from luna_sdk.schemas.solution import (
    Result,
    Solution,
    UseCaseRepresentation,
    UseCaseResult,
)
from luna_sdk.utils.parameter_finder import get_parameter_by_solver
from luna_sdk.utils.qpu_tokens import extract_qpu_tokens_from_env


class SolutionsRepo(ISolutionsRepo):
    _endpoint = "/solutions"

    def get(self, solution_id: str, **kwargs) -> Solution:
        response = self._client.get(f"{self._endpoint}/{solution_id}", **kwargs)

        response.raise_for_status()

        return Solution.model_validate_json(response.text)

    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        limit: int = 50,
        offset: int = 0,
        optimization_id: Optional[str] = None,
        **kwargs,
    ) -> List[Solution]:
        params = {}
        if timeframe and timeframe != TimeframeEnum.all_time:  # no value == all_time
            params["timeframe"] = timeframe.value

        if limit < 1:
            # set the minimum limit to 1
            limit = 1

        if optimization_id is not None:
            params["optimization_id"] = str(optimization_id)

        params["limit"] = str(limit)
        params["offset"] = str(offset)
        response = self._client.get(self._endpoint, params=params, **kwargs)

        response.raise_for_status()

        return [Solution.model_validate(i) for i in response.json()]

    def delete(self, solution_id: str, **kwargs) -> None:
        self._client.delete(f"{self._endpoint}/{solution_id}", **kwargs)

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
        if qpu_tokens is not None:
            rest_qpu_tokens = RestAPITokenProvider.from_sdk_token_provider(
                TokenProvider.model_validate(qpu_tokens)
            )
        else:
            rest_qpu_tokens = None
        # try to retrieve qpu tokens from env variables
        if rest_qpu_tokens is None:
            rest_qpu_tokens = extract_qpu_tokens_from_env()

        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        params = SolutionsRepo.validate_solver_params(
            solver_name, provider, solver_parameters, fail_on_invalid_params
        )

        solution_in = SolutionIn(
            optimization=optimization_id,
            solver_name=solver_name,
            provider=provider,
            parameters=params,
            qpu_tokens=rest_qpu_tokens,
            encryption_key=encryption_key,
            name=name,
        )
        response = self._client.post(
            self._endpoint, content=solution_in.model_dump_json(), **kwargs
        )
        response.raise_for_status()

        return Solution.model_validate_json(response.text)

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
        # First create the solution
        params = SolutionsRepo.validate_solver_params(
            solver_name, provider, solver_parameters, fail_on_invalid_params
        )

        solution: Solution = self.create(
            optimization_id=optimization_id,
            solver_name=solver_name,
            provider=provider,
            solver_parameters=params,
            qpu_tokens=qpu_tokens,
            encryption_key=encryption_key,
            name=name,
            **kwargs,
        )
        # times are in sec

        cur_sleep_time: float

        if sleep_time_initial > 0.0:
            cur_sleep_time = sleep_time_initial
        else:
            cur_sleep_time = 5.0
            logging.warning(
                f"Invalid sleep_time_initial: {sleep_time_initial}, setting it to default value {cur_sleep_time}"
            )

        while (
            solution.status == StatusEnum.REQUESTED
            or solution.status == StatusEnum.IN_PROGRESS
        ):
            logging.info(
                f"Waiting for solution {solution.id} to complete, "
                f"current status: {solution.status}"
                f", sleeping for {cur_sleep_time} seconds."
            )
            sleep(cur_sleep_time)
            cur_sleep_time += sleep_time_increment
            if cur_sleep_time > sleep_time_max:
                cur_sleep_time = sleep_time_max

            solution = self.get(solution_id=solution.id, **kwargs)

        return solution

    def get_use_case_representation(
        self, solution_id: str, **kwargs
    ) -> UseCaseRepresentation:
        response = self._client.get(
            f"{self._endpoint}/{solution_id}/representation", **kwargs
        )
        response.raise_for_status()
        return UseCaseRepresentation.model_validate_json(response.text)

    def get_best_result(self, solution: Solution) -> Optional[Result]:
        if solution.results is None or solution.sense is None:
            return None

        agg = min if solution.sense == SenseEnum.MIN else max
        best_result = agg(solution.results, key=lambda x: x.obj_value)

        return best_result

    def get_best_use_case_result(
        self, use_case_representation: UseCaseRepresentation
    ) -> Optional[UseCaseResult]:
        if (
            use_case_representation.results is None
            or use_case_representation.sense is None
        ):
            return None

        agg = min if use_case_representation.sense == SenseEnum.MIN else max
        best_result = agg(use_case_representation.results, key=lambda x: x.obj_value)

        return best_result

    @staticmethod
    def validate_solver_params(
        solver: str,
        provider: str,
        solver_parameter: Optional[Union[Dict[str, Any], BaseModel]],
        fail_on_invalid_params: bool = True,
    ) -> Dict[str, Any]:
        """
        This function checks if the params provided are valid for the provided solver
        and provider.
        If no parameter class was found, there will be no check.

        Parameters
        ----------
        solver: str
            The solver
        provider: str
            The provider
        solver_parameter: Optional[Union[Dict[str, Any], BaseModel]]
            The solver parameter
        fail_on_invalid_params: bool
            Default true.
            If True, a ValueError will be raised, if the solver_parameter are invalid.
            Otherwise, there will only a warning.

        Returns
        -------
        Dict[str, Any]
            Validated solver params

        Raises
        -------
        ValidationError
            If the object could not be validated.

        """
        if solver_parameter is None:
            logging.info(
                "You didn't provide any specific solver parameters, so we chose the "
                "default ones for this solver."
            )
            return {}

        params: Dict[str, Any]
        if isinstance(solver_parameter, BaseModel):
            params = solver_parameter.dict()
        else:
            params = solver_parameter

        parameter_class: Optional[Type[BaseModel]] = get_parameter_by_solver(
            solver, provider
        )

        if parameter_class is None:
            logging.info(
                f"SDK was not able to find a parameter for solver {solver} "
                f"and provider {provider}."
            )
            return params

        try:
            parameter_class.model_validate(params)

        except ValidationError as e:
            if fail_on_invalid_params:
                raise e
            logging.warning(
                "The validation for the provided solver parameter failed.\n"
                f"Detected error:\n{e}\n"
                "Since continue on error is enabled, no error was raised.\n"
                "Solving with Luna can still fail due to the parameters."
            )
        return params
