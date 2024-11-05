from typing import List

from pydantic import BaseModel


class QuboSchema(BaseModel):
    matrix: List[List[float]]
    offset: float
