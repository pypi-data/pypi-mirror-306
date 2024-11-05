from typing import List, Dict

from pydantic import BaseModel

from luna_sdk.schemas.transformations.bqm import BQMInverter


class MatrixSchema(BaseModel):
    matrix: List[List[float]]
    variable_indices: Dict[str, int]

    inverter: BQMInverter
