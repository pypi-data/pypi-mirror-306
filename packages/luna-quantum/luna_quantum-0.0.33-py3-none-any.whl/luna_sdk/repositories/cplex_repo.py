import os
import pickle
import tempfile
from functools import partial
from typing import Dict, List, Tuple

import dimod
from dimod import ConstrainedQuadraticModel
from dimod.constrained.constrained import CQMToBQMInverter
from docplex.mp.model import Model as DOCplexModel
from qiskit_optimization import QuadraticProgram

from luna_sdk.exceptions.transformation import TransformationException
from luna_sdk.interfaces.cplex_repo_i import ICplexRepo
from luna_sdk.schemas.transformations.bqm import BQMResultSchema
from luna_sdk.schemas.transformations.matrix import MatrixSchema


class CplexRepo(ICplexRepo):
    _endpoint = "/transformations/docplex"

    def _send_request_with_pickle_file_response(
        self, docplex_model: DOCplexModel, endpoint: str, **kwargs
    ):
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "wb") as tmp:
            pickle.dump(docplex_model, tmp)
        response = self._client.post(
            endpoint, files={"file": (file.name, file.file)}, **kwargs
        )
        os.remove(file.name)
        try:
            parsed_model = pickle.loads(response.content)
        except Exception:
            raise TransformationException()
        return parsed_model

    def to_qubo_qiskit(self, docplex_model: DOCplexModel, **kwargs) -> QuadraticProgram:
        qubo_qiskit_model = self._send_request_with_pickle_file_response(
            docplex_model, f"{self._endpoint}/to-qubo-qiskit", **kwargs
        )
        try:
            assert isinstance(qubo_qiskit_model, QuadraticProgram)
        except AssertionError:
            raise TransformationException()
        return qubo_qiskit_model

    def to_lp_file(self, docplex_model: DOCplexModel, filepath: str, **kwargs) -> None:
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "wb") as tmp:
            pickle.dump(docplex_model, tmp)
        response = self._client.post(
            f"{self._endpoint}/to-lp-file",
            files={"file": (file.name, file.file)},
            **kwargs,
        )
        with open(filepath, "w") as file:  # type: ignore
            file.write(response.content.decode("utf-8"))  # type: ignore

    def to_lp_string(self, docplex_model: DOCplexModel, **kwargs) -> str:
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "wb") as tmp:
            pickle.dump(docplex_model, tmp)
        response = self._client.post(
            f"{self._endpoint}/to-lp-file",
            files={"file": (file.name, file.file)},
            **kwargs,
        )
        return response.content.decode("utf-8")

    def to_qubo_matrix(
        self, docplex_model: DOCplexModel, **kwargs
    ) -> Tuple[List[List[float]], partial]:
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "wb") as tmp:
            pickle.dump(docplex_model, tmp)
        response = self._client.post(
            f"{self._endpoint}/to-qubo-matrix",
            files={"file": (file.name, file.file)},
            **kwargs,
        )
        retrieved_matrix = MatrixSchema.model_validate(response.json())
        return retrieved_matrix.matrix, partial(
            self.inverter,
            var_indices=retrieved_matrix.variable_indices,
            inverter_bqm=CQMToBQMInverter.from_dict(
                retrieved_matrix.inverter.model_dump()
            ),
        )

    def to_bqm(
        self, docplex_model: DOCplexModel, **kwargs
    ) -> Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]:
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "wb") as tmp:
            pickle.dump(docplex_model, tmp)
        response = self._client.post(
            f"{self._endpoint}/to-bqm", files={"file": (file.name, file.file)}, **kwargs
        )
        retrieved_bqm = BQMResultSchema.model_validate(response.json())

        quadratic: Dict[Tuple[str, str], float] = {}
        for key, value in retrieved_bqm.bqm.quadratic.items():
            split_key = tuple(key.split(","))
            if len(split_key) != 2:
                raise TransformationException
            quadratic[split_key[0], split_key[1]] = value
        try:
            bqm = dimod.BinaryQuadraticModel(
                retrieved_bqm.bqm.linear,
                quadratic,
                offset=retrieved_bqm.bqm.offset,
                vartype=retrieved_bqm.bqm.var_type,
            )
        except Exception:
            raise TransformationException()
        inverter = CQMToBQMInverter.from_dict(retrieved_bqm.inverter.model_dump())
        return bqm, inverter

    def to_cqm(
        self, docplex_model: DOCplexModel, **kwargs
    ) -> ConstrainedQuadraticModel:
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "wb") as tmp:
            pickle.dump(docplex_model, tmp)
        response = self._client.post(
            f"{self._endpoint}/to-cqm", files={"file": (file.name, file.file)}, **kwargs
        )
        cqm = ConstrainedQuadraticModel.from_file(response.content)
        return cqm
