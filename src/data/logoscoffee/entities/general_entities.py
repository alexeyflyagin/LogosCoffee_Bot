from dataclasses import dataclass
from enum import Enum

from src.data.logoscoffee.entities.orm_entities import ProductEntity, OrderEntity


@dataclass
class MenuEntity:
    all_products: list[ProductEntity]


@dataclass
class OrderUpdateEntity:
    order: OrderEntity
    update_type: 'UpdateType'

    class UpdateType(Enum):
        STATE__PENDING = 0
        STATE__COOKING = 1
        STATE__READY = 2
        STATE__COMPLETED = 3
        STATE__CANCELED = 4
