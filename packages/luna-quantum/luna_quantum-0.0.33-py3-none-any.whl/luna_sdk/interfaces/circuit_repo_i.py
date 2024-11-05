from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas.circuit import CircuitJob, CircuitResult
from luna_sdk.schemas.enums.circuit import CircuitProviderEnum
from luna_sdk.schemas.qpu_token import TokenProvider


class ICircuitRepo(IRepository, ABC):
    @abstractmethod
    def create(
        self,
        circuit: str,
        provider: CircuitProviderEnum,
        params: Dict[str, Any] = {},
        qpu_tokens: Optional[TokenProvider] = None,
        encryption_key: Optional[str] = None,
        **kwargs,
    ) -> CircuitJob:
        """
        Create a circuit solution.

        Parameters
        ----------
        circuit: str
            The circuit which to create a solution for.
        provider: CircuitProviderEnum
            Which provider to use to solve the circuit.
        params: Dict[str, Any]
            Additional parameters of the circuit.
        qpu_tokens: Optional[TokenProvider]
            The tokens to be used for the QPU.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        CircuitJob
            The created circuit job.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        job: CircuitJob,
        encryption_key: Optional[str] = None,
        **kwargs,
    ) -> CircuitResult:
        """
        Get the result of a circuit.

        Parameters
        ----------
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        CircuitResult
            The result of solving the circuit.
        """
        raise NotImplementedError
