from uuid import uuid4
from app.storage.memory import customers, items, invoices
from app.models.invoice import Invoice

def calculate_total(invoice_items):
    total = 0
    for i in invoice_items:
        item = items.get(i.item_id)
        total += item.price * i.quantity
    return total

def create_invoice(customer_id, invoice_items):
    total = calculate_total(invoice_items)
    invoice = Invoice(
        id=uuid4(),
        customer_id=customer_id,
        items=invoice_items,
        total_amount=total
    )
    invoices[invoice.id] = invoice
    return invoice
