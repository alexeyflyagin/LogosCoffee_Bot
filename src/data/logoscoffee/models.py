from pydantic import BaseModel


class PlaceOrderData(BaseModel):
    details: str
