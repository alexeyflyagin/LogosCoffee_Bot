from enum import IntEnum, auto

TOKEN = "token"
EVENT__NEW_ORDER = "newOrder"


class Tag(IntEnum):
    NEXT_ORDER_CONFIRMATION = auto()
