from pydantic import BaseModel


class PlaceOrderData(BaseModel):
    details: str


class CancelOrderData(BaseModel):
    details: str
