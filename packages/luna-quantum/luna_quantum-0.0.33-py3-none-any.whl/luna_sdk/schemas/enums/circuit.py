from enum import Enum


class CircuitProviderEnum(str, Enum):
    IBM = "ibm"
    QCTRL = "qctrl"
    AWS = "aws"


class CircuitStatusEnum(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
