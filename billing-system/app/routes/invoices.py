from fastapi import APIRouter
from uuid import UUID
from typing import List
from app.models.invoice import InvoiceItem
from app.services.billing_service import create_invoice
from app.storage.memory import invoices

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/")
def generate_invoice(customer_id: UUID, items: List[InvoiceItem]):
    return create_invoice(customer_id, items)

@router.get("/")
def list_invoices():
    return list(invoices.values())
