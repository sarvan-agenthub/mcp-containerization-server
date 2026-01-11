from pydantic import BaseModel
from uuid import UUID
from typing import List

class InvoiceItem(BaseModel):
    item_id: UUID
    quantity: int

class Invoice(BaseModel):
    id: UUID
    customer_id: UUID
    items: List[InvoiceItem]
    total_amount: float
