from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class OptimizationSense(str, Enum):
    Max = "max"
    Min = "min"


class VariableTypes(str, Enum):
    Binary = "B"
    Integer = "I"
    Float = "F"


class ConstraintTypes(str, Enum):
    OneHot = "one-hot"
    Arithmetic = "arithemtic"
    Soft = "soft"


class ModelSpecs(BaseModel):
    """Serialized Model specs"""

    max_degree: int
    min_degree: int
    needed_constraints: List[ConstraintTypes]
    can_handle_constraints: List[ConstraintTypes]
    can_handle_vtype: List[VariableTypes]
    can_handle_sense: List[OptimizationSense]


class SolverInfo(BaseModel):
    full_name: str
    short_name: str
    available: bool
    params: dict
    description: Optional[str]
    specs: ModelSpecs
