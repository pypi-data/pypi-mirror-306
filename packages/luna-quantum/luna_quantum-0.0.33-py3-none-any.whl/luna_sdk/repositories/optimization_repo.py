import json
from io import BufferedReader
from typing import Any, Dict, List, Optional, Type

from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel
from httpx import Response

from luna_sdk.interfaces.optimization_repo_i import IOptimizationRepo
from luna_sdk.schemas import UseCase
from luna_sdk.schemas.create import QUBOIn
from luna_sdk.schemas.create.optimization import OptimizationUseCaseIn
from luna_sdk.schemas.enums.optimization import OptFormat
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.optimization import (
    Optimization,
    OptimizationBQM,
    OptimizationCQM,
    OptimizationLP,
    OptimizationUseCase,
    OptimizationQubo,
)
from luna_sdk.schemas.optimization_formats.bqm import BQMSchema
from luna_sdk.schemas.optimization_formats.cqm import CQMSchema


class OptimizationRepo(IOptimizationRepo):
    @property
    def _endpoint(self) -> str:
        return "/optimizations"

    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        input_type: Optional[OptFormat] = None,
        limit: int = 50,
        offset: int = 0,
        **kwargs,
    ) -> List[Optimization]:
        params = {}
        if timeframe and timeframe != TimeframeEnum.all_time:  # no value == all_time
            params["timeframe"] = timeframe.value

        if input_type:
            params["original_format"] = input_type.value

        if limit < 1:
            # set the minimum limit to 1
            limit = 1

        params["limit"] = str(limit)
        params["offset"] = str(offset)
        response: Response = self._client.get(self._endpoint, params=params, **kwargs)
        response.raise_for_status()
        return [Optimization.model_validate(item) for item in response.json()]

    def get(self, optimization_id: str, **kwargs) -> Optimization:
        response: Response = self._client.get(
            f"{self._endpoint}/{optimization_id}", **kwargs
        )
        response.raise_for_status()
        response_data = response.json()

        model: Type[Optimization] = Optimization

        optimization_data = response_data.pop("optimization_data", None)
        if optimization_data:
            original_format = response_data["original_format"]

            if original_format == OptFormat.BQM:
                model = OptimizationBQM
            elif original_format == OptFormat.CQM:
                model = OptimizationCQM
            elif original_format == OptFormat.LP:
                model = OptimizationLP
            elif original_format == OptFormat.QUBO:
                if response_data.get("use_case_name"):
                    model = OptimizationUseCase
                else:
                    model = OptimizationQubo
            else:
                raise ValueError("Unknown optimization format")

            response_data.update(optimization_data)

        return model.model_validate(response_data)

    def create_from_qubo(
        self, name: str, matrix: List[List[float]], **kwargs
    ) -> Optimization:
        data_in: Dict[str, Any] = QUBOIn(name=name, matrix=matrix).model_dump()

        response: Response = self._client.post(
            f"{self._endpoint}/qubo", json=data_in, **kwargs
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_use_case(
        self, name: str, use_case: UseCase, **kwargs
    ) -> Optimization:
        optimization_in = OptimizationUseCaseIn(
            name=name, use_case=use_case, params=None
        )

        response: Response = self._client.post(
            f"{self._endpoint}/use_case",
            content=optimization_in.model_dump_json(),
            **kwargs,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_bqm(
        self, name: str, bqm: BinaryQuadraticModel, **kwargs
    ) -> Optimization:
        data_in = {"name": name, **BQMSchema.from_bqm(bqm).model_dump()}

        response: Response = self._client.post(
            f"{self._endpoint}/bqm", json=data_in, **kwargs
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_cqm(
        self, name: str, cqm: ConstrainedQuadraticModel, **kwargs
    ) -> Optimization:
        data_in = {"name": name, **CQMSchema.from_cqm(cqm).model_dump()}

        response: Response = self._client.post(
            f"{self._endpoint}/cqm", json=data_in, **kwargs
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_lp_file(
        self, name: str, lp_file: BufferedReader, **kwargs
    ) -> Optimization:
        response: Response = self._client.post(
            f"{self._endpoint}/lp-file",
            data={"optimization_in": json.dumps({"name": name})},
            files={"lp_file": lp_file},
            **kwargs,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_lp_string(
        self, name: str, lp_string: str, **kwargs
    ) -> Optimization:
        data_in = {"name": name, "lp_string": lp_string}

        response: Response = self._client.post(
            f"{self._endpoint}/lp-string", json=data_in, **kwargs
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def rename(self, optimization_id: str, name: str, **kwargs) -> Optimization:
        data: Dict[str, str] = {"name": name}

        response: Response = self._client.put(
            f"{self._endpoint}/{optimization_id}", content=json.dumps(data), **kwargs
        )
        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def delete(self, optimization_id: str, **kwargs) -> None:
        response: Response = self._client.delete(
            f"{self._endpoint}/{optimization_id}", **kwargs
        )
        response.raise_for_status()
