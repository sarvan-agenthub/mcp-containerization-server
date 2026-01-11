from fastapi import APIRouter
from uuid import uuid4
from app.models.customer import Customer
from app.storage.memory import customers

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/")
def create_customer(name: str, email: str):
    customer = Customer(id=uuid4(), name=name, email=email)
    customers[customer.id] = customer
    return customer

@router.get("/")
def list_customers():
    return list(customers.values())
