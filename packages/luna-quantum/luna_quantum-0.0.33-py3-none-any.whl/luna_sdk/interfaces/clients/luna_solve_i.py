from abc import ABC, abstractmethod

from luna_sdk.interfaces.clients.client_i import IClient
from luna_sdk.interfaces.info_repo_i import IInfoRepo
from luna_sdk.interfaces.optimization_repo_i import IOptimizationRepo
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.interfaces.solutions_repo_i import ISolutionsRepo


class ILunaSolve(IClient, ABC):
    @property
    @abstractmethod
    def optimization(self) -> IOptimizationRepo:
        """
        Returns an optimization repository

        Returns
        ----------
            IOptimizationRepo]

        """
        raise NotImplementedError

    @property
    @abstractmethod
    def solution(self) -> ISolutionsRepo:
        raise NotImplementedError

    @property
    @abstractmethod
    def qpu_token(self) -> IQpuTokenRepo:
        raise NotImplementedError

    @property
    @abstractmethod
    def info(self) -> IInfoRepo:
        raise NotImplementedError
