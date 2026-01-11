from pydantic import BaseModel
from uuid import UUID

class Item(BaseModel):
    id: UUID
    name: str
    price: float
