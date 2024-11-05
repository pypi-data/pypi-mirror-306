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
from luna_sdk.interfaces.lp_repo_i import ILPRepo
from luna_sdk.schemas.transformations.bqm import BQMResultSchema
from luna_sdk.schemas.transformations.matrix import MatrixSchema


class LPRepo(ILPRepo):
    _endpoint = "/transformations/lp"

    def _send_request_with_pickle_file_response(self, lp_string: str, endpoint: str):
        file = tempfile.NamedTemporaryFile(delete=False, suffix=".lp")
        with open(file.name, "w") as tmp:
            tmp.write(lp_string)
        response = self._client.post(endpoint, files={"file": (file.name, file.file)})
        os.remove(file.name)
        try:
            parsed_model = pickle.loads(response.content)
        except Exception:
            raise TransformationException()
        return parsed_model

    def to_qubo_qiskit(self, lp_string: str, **kwargs) -> QuadraticProgram:
        qubo_qiskit_model = self._send_request_with_pickle_file_response(
            lp_string, f"{self._endpoint}/to-qubo-qiskit", **kwargs
        )
        try:
            assert isinstance(qubo_qiskit_model, QuadraticProgram)
        except AssertionError:
            raise TransformationException()
        return qubo_qiskit_model

    def to_docplex(self, lp_string: str, **kwargs) -> DOCplexModel:
        docplex_model = self._send_request_with_pickle_file_response(
            lp_string, f"{self._endpoint}/to-docplex", **kwargs
        )
        try:
            assert isinstance(docplex_model, DOCplexModel)
        except AssertionError:
            raise TransformationException()
        return docplex_model

    def to_qubo_matrix(
        self, lp_string: str, **kwargs
    ) -> Tuple[List[List[float]], partial]:
        file = tempfile.NamedTemporaryFile(delete=False, suffix=".lp")
        with open(file.name, "w") as tmp:
            tmp.write(lp_string)
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
        self, lp_string: str, **kwargs
    ) -> Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]:
        file = tempfile.NamedTemporaryFile(delete=False, suffix=".lp")
        with open(file.name, "w") as tmp:
            tmp.write(lp_string)
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
        inverter = CQMToBQMInverter.from_dict(retrieved_bqm.inverter.dict())
        return bqm, inverter

    def to_cqm(self, lp_string: str, **kwargs) -> ConstrainedQuadraticModel:
        file = tempfile.NamedTemporaryFile(delete=False, suffix=".lp")
        with open(file.name, "w") as tmp:
            tmp.write(lp_string)
        response = self._client.post(
            f"{self._endpoint}/to-cqm", files={"file": (file.name, file.file)}, **kwargs
        )
        cqm = ConstrainedQuadraticModel.from_file(response.content)
        return cqm
