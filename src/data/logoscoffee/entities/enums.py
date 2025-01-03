from enum import Enum


class OrderState(Enum):
    CREATED = 0
    PENDING = 1
    COOKING = 2
    READY = 3
    COMPLETED = 4
    CANCELED = 5


class OrderStateGroup(Enum):
    DRAFT = 0
    IN_PROGRESS = 1
    CLOSED = 2
