from abc import ABC, abstractmethod

from src.data.logoscoffee.models import PlaceOrderData


class ClientAndOrderService(ABC):

    @abstractmethod
    async def PlaceOrder(
            self,
            token: str,
            data: PlaceOrderData,
    ):
        pass