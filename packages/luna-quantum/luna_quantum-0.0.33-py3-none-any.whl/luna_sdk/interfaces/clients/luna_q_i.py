from abc import ABC, abstractmethod

from luna_sdk.interfaces import ICircuitRepo
from luna_sdk.interfaces.clients.client_i import IClient
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo


class ILunaQ(IClient, ABC):
    """
    Interface for the LunaQ client


    """

    @property
    @abstractmethod
    def qpu_token(self) -> IQpuTokenRepo:
        """
        Returns a QPU token repository

        Examples
        --------
            >>> add(4.0, 2.0)
            6.0
            >>> add(4, 2)
            6.0


        """

        raise NotImplementedError

    @property
    @abstractmethod
    def circuit(self) -> ICircuitRepo:
        """
        Returns a circuit :py:class: repository
        """
        raise NotImplementedError
