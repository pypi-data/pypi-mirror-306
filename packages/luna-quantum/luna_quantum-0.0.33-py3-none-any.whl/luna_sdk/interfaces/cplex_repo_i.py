from abc import ABC, abstractmethod
from functools import partial
from typing import List, Tuple

import dimod
from dimod import ConstrainedQuadraticModel
from dimod.constrained.constrained import CQMToBQMInverter
from docplex.mp.model import Model as DOCplexModel
from qiskit_optimization import QuadraticProgram

from luna_sdk.interfaces import IRepository


class ICplexRepo(IRepository, ABC):
    @staticmethod
    def inverter(sample, var_indices, inverter_bqm) -> CQMToBQMInverter:
        sample_list = list(sample.values())
        var_sample = {name: sample_list[index] for name, index in var_indices.items()}
        return inverter_bqm(var_sample)

    @abstractmethod
    def to_qubo_qiskit(self, docplex_model: DOCplexModel, **kwargs) -> QuadraticProgram:
        """
        Transform DOCplex model to QUBO Qiskit

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        QuadraticProgram
            QUBO Qiskit representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_lp_file(self, docplex_model: DOCplexModel, filepath: str, **kwargs) -> None:
        """
        Transform DOCplex to LP representation

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        filepath: str
            .lp file path where result should be stored
        **kwargs
            Parameters to pass to `httpx.request`.
        """
        raise NotImplementedError

    @abstractmethod
    def to_lp_string(self, docplex_model: DOCplexModel, **kwargs) -> str:
        """
        Transform DOCplex to LP representation

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        str
            LP representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_qubo_matrix(
        self, docplex_model: DOCplexModel, **kwargs
    ) -> Tuple[List[List[float]], partial]:
        """
        Transform DOCplex model to QUBO matrix

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Tuple[List[List[float]], partial]
            QUBO matrix representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_bqm(
        self, docplex_model: DOCplexModel, **kwargs
    ) -> Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]:
        """
        Transform DOCplex model to BQM model

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]
            BQM representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_cqm(
        self, docplex_model: DOCplexModel, **kwargs
    ) -> ConstrainedQuadraticModel:
        """
        Transform DOCplex model to CQM model

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        ConstrainedQuadraticModel
            CQM representation
        """
        raise NotImplementedError
