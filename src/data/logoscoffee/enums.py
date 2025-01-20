from enum import Enum


class OrderState(Enum):
    PENDING = 0
    COOKING = 1
    READY = 2
    COMPLETED = 3
    CANCELED = 4


class OrderStateGroup(Enum):
    IN_PROGRESS = 0
    CLOSED = 1
