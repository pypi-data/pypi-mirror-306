from enum import Enum


class StatusEnum(str, Enum):
    REQUESTED = "REQUESTED"
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELED"
