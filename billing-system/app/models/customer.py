from pydantic import BaseModel
from uuid import UUID

class Customer(BaseModel):
    id: UUID
    name: str
    email: str
