from enum import Enum
from typing import Dict

from pydantic import BaseModel, ConfigDict


class VarTypeStrEnum(str, Enum):
    SPIN = "SPIN"
    BINARY = "BINARY"
    INTEGER = "INTEGER"
    DISCRETE = "DISCRETE"
    REAL = "REAL"


class BQMSchema(BaseModel):
    linear: Dict[str, float]
    quadratic: Dict[str, float]
    offset: float
    var_type: VarTypeStrEnum


class BQMInverter(BaseModel):
    binary: Dict[str, VarTypeStrEnum]
    integers: Dict[str, BQMSchema]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BQMResultSchema(BaseModel):
    bqm: BQMSchema
    inverter: BQMInverter

    model_config = ConfigDict(arbitrary_types_allowed=True)
