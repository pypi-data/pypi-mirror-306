from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Dict, List, Tuple

import dimod
from dimod import ConstrainedQuadraticModel
from dimod.constrained.constrained import CQMToBQMInverter
from docplex.mp.model import Model as DOCplexModel
from qiskit_optimization import QuadraticProgram

from luna_sdk.interfaces import IRepository


class ILPRepo(IRepository, ABC):
    @staticmethod
    def inverter(sample, var_indices, inverter_bqm) -> CQMToBQMInverter:
        sample_list = list(sample.values())
        var_sample = {name: sample_list[index] for name, index in var_indices.items()}
        return inverter_bqm(var_sample)

    @abstractmethod
    def to_qubo_qiskit(self, lp_string: str, **kwargs) -> QuadraticProgram:
        """
        Transform LP to QUBO Qiskit

        Parameters
        ----------
        lp_string: str
            LP problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        QuadraticProgram
            QUBO Qiskit representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_docplex(self, lp_string: str, **kwargs) -> DOCplexModel:
        """
        Transform LP to DOCplex

        Parameters
        ----------
        lp_string: str
            LP problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        DOCplexModel
            DOCplex representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_qubo_matrix(
        self, lp_string: str, **kwargs
    ) -> Tuple[List[List[float]], partial]:
        """
        Transform LP to QUBO matrix

        Parameters
        ----------
        lp_string: str
            LP problem description
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
        self, lp_string: str, **kwargs
    ) -> Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]:
        """
        Transform LP to BQM model

        Parameters
        ----------
        lp_string: str
            LP problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]
            BQM representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_cqm(self, lp_string: str, **kwargs) -> ConstrainedQuadraticModel:
        """
        Transform LP to CQM model

        Parameters
        ----------
        lp_string: str
            LP problem description
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        ConstrainedQuadraticModel
            CQM representation
        """
        raise NotImplementedError
