from typing import List

from pydantic import BaseModel


class QUBOIn(BaseModel):
    """
    Pydantic model for QUBO

    Attributes
    ----------
    name: str
        Name of the Model
    matrix: List[List[float]]
        QUBO matrix
    """

    name: str
    matrix: List[List[float]]
