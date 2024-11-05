from enum import Enum
from typing import Optional

from dimod import BinaryQuadraticModel

from luna_sdk.schemas.optimization_formats.qm import QMSchema


class BQMVarType(str, Enum):
    SPIN = "SPIN"
    BINARY = "BINARY"


class BQMSchema(QMSchema):
    vartype: BQMVarType
    offset: Optional[float] = None

    @classmethod
    def from_bqm(cls, bqm: BinaryQuadraticModel) -> "BQMSchema":
        return cls(
            vartype=BQMVarType(bqm.vartype.name),
            quadratic={k: v for k, v in bqm.quadratic.items()},
            linear={k: v for k, v in bqm.linear.items()},
            offset=float(bqm.offset) if bqm.offset is not None else None,
        )

    def to_bqm(self) -> BinaryQuadraticModel:
        bqm = BinaryQuadraticModel(
            self.linear,
            self._parsed_quadratic,
            offset=self.offset,
            vartype=self.vartype,
        )
        return bqm
