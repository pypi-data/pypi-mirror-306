from enum import Enum


class OptFormat(str, Enum):
    """Enumeration of all supported formats."""

    AQ_MODEL = "AQ_MODEL"
    LP = "LP"
    QUBO = "QUBO_MATRIX"
    CQM = "CQM"
    BQM = "BQM"
