from fastapi import FastAPI
from app.core.config import settings
from app.routes import customers, items, invoices

app = FastAPI(
    title=settings.app_name,
    version=settings.version
)

app.include_router(customers.router)
app.include_router(items.router)
app.include_router(invoices.router)

@app.get("/health")
def health():
    return {"status": "ok"}
