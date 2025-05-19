from pydantic import BaseModel
from datetime import datetime


class InventoryStatus(BaseModel):
    product_id: int
    product_name: str
    quantity: float
    min_stock_level: float

    class Config:
        orm_mode = True


class InventoryChangeCreate(BaseModel):
    product_id: int
    change_amount: float
    name: str | None = None


class InventoryChangeRead(BaseModel):
    id: int
    product_id: int
    change_amount: float
    name: str | None = None
    changed_at: datetime

    class Config:
        from_attributes = True
