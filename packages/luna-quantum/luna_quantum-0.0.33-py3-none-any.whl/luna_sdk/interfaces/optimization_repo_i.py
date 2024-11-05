from abc import ABC, abstractmethod
from io import BufferedReader
from typing import List, Optional

from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas.enums.optimization import OptFormat
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.optimization import Optimization
from luna_sdk.schemas.solution import Numeric
from luna_sdk.schemas.use_cases import UseCase


class IOptimizationRepo(IRepository, ABC):
    @abstractmethod
    def get(self, optimization_id: str, **kwargs) -> Optimization:
        """
        Retrieve a optimization by id.

        Parameters
        ----------
        optimization_id: str
            Id of the optimization to be retrieved.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        input_type: Optional[OptFormat] = None,
        limit: int = 50,
        offset: int = 0,
        **kwargs,
    ) -> List[Optimization]:
        """
        Retrieve a list of optimizations.

        Parameters
        ----------
        timeframe: Optional[TimeframeEnum]
            Only return optimizations created within a specified timeframe.
            Default None.
        input_type: Optional[OptFormat]
            Only return optimizations of a specified input type. Default None.
        limit:
            Limit the number of optimizations to be returned. Default value 50.
        offset:
            Offset the list of optimizations by this amount. Default value 0.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        List[Optimization]:
            List of optimizations.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_qubo(
        self, name: str, matrix: List[List[Numeric]], **kwargs
    ) -> Optimization:
        """
        Create an optimization from a QUBO matrix.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        matrix: List[List[float]]
            QUBO matrix.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_use_case(
        self, name: str, use_case: UseCase, **kwargs
    ) -> Optimization:
        """
        Create an optimization from a use case.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        use_case: UseCase
            Use case.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_bqm(
        self, name: str, bqm: BinaryQuadraticModel, **kwargs
    ) -> Optimization:
        """
        Create an optimization from BQM.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        bqm: BinaryQuadraticModel
            QUBO in dimod BQM format.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_cqm(
        self, name: str, cqm: ConstrainedQuadraticModel, **kwargs
    ) -> Optimization:
        """
        Create an optimization from CQM.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        cqm: ConstrainedQuadraticModel
            in dimod CQM format.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_lp_file(
        self, name: str, lp_file: BufferedReader, **kwargs
    ) -> Optimization:
        """
        Create an optimization from LP file.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        lp_file: buffer reader.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_lp_string(
        self, name: str, lp_string: str, **kwargs
    ) -> Optimization:
        """
        Create an optimization from LP file.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        lp_string: string.
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def rename(self, optimization_id: str, name: str, **kwargs) -> Optimization:
        """
        Update the name of the optimization

        Parameters
        ----------
        optimization_id: str
            Id of the optimization to be updated.
        name: str
            New name of the optimization
        **kwargs
            Parameters to pass to `httpx.request`.

        Returns
        -------
        Optimization:
            Updated optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, optimization_id: str, **kwargs) -> None:
        """
        Delete an optimization by id.

        Parameters
        ----------
        optimization_id: str
            Id of the optimization to be deleted.
        **kwargs
            Parameters to pass to `httpx.request`.
        """
        raise NotImplementedError
