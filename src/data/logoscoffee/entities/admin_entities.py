from datetime import datetime

from attr import dataclass
from pydantic import BaseModel


@dataclass
class ReviewEntity(BaseModel):
    id: int
    date_create: datetime
    text_content: str

    class Config:
        from_attributes = True
