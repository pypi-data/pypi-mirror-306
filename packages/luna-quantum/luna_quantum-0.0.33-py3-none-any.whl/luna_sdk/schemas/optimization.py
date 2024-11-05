from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from luna_sdk.schemas.enums.optimization import OptFormat
from luna_sdk.schemas.optimization_formats.bqm import BQMSchema
from luna_sdk.schemas.optimization_formats.cqm import CQMSchema
from luna_sdk.schemas.optimization_formats.lp import LPSchema
from luna_sdk.schemas.optimization_formats.qubo import QuboSchema
from luna_sdk.schemas.pretty_base import PrettyBase
from luna_sdk.schemas.wrappers import PydanticDatetimeWrapper


class Optimization(PrettyBase):
    """
    Pydantic model for optimization going OUT.
        Attributes
    ----------
    id: str
        Id of the optimization
    created_date: Optional[DatetimeWrapper]
        Date when optimization was created
    created_by: Optional[str]
        Id of the user who created optimization
    modified_date: Optional[DatetimeWrapper]
        Date when optimization was modified
    modified_by: Optional[str]
        Id of the user who modified optimization
    """

    id: str
    name: Optional[str] = None
    created_date: PydanticDatetimeWrapper
    created_by: str
    modified_date: Optional[PydanticDatetimeWrapper] = None
    modified_by: Optional[str] = None
    original_format: Optional[OptFormat] = None
    use_case_name: Optional[str] = None
    params: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="ignore", from_attributes=False)


class OptimizationBQM(Optimization, BQMSchema): ...


class OptimizationCQM(Optimization, CQMSchema): ...


class OptimizationLP(Optimization, LPSchema): ...


class OptimizationUseCase(Optimization, QuboSchema):
    use_case: Dict[str, Any]


class OptimizationQubo(Optimization, QuboSchema): ...


T = TypeVar("T")


class OptimizationCreate(BaseModel, Generic[T]):
    """Pydantic model for optimization coming IN."""

    instance: T
