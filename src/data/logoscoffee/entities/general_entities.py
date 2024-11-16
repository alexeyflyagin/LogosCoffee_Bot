from dataclasses import dataclass

from src.data.logoscoffee.entities.orm_entities import ProductEntity


@dataclass
class MenuEntity:
    all_products: list[ProductEntity]
