from fastapi import APIRouter
from uuid import uuid4
from app.models.item import Item
from app.storage.memory import items

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/")
def create_item(name: str, price: float):
    item = Item(id=uuid4(), name=name, price=price)
    items[item.id] = item
    return item

@router.get("/")
def list_items():
    return list(items.values())

