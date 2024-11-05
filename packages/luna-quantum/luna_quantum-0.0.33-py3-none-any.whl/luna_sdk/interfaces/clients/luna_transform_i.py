from abc import abstractmethod, ABC

from luna_sdk.interfaces import IClient, IOptimizationRepo
from luna_sdk.interfaces.cplex_repo_i import ICplexRepo
from luna_sdk.interfaces.lp_repo_i import ILPRepo


class ILunaTransform(IClient, ABC):
    @property
    @abstractmethod
    def cplex(self) -> ICplexRepo:
        """
        Returns an docplex repository

        Returns
        ----------
            ICplexRepo

        """
        raise NotImplementedError

    @property
    @abstractmethod
    def lp(self) -> ILPRepo:
        """
        Returns a lp repository

        Returns
        ----------
            ILPRepo

        """
        raise NotImplementedError
