from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    sku: str
    category: str
    price: float

class ProductCreate(ProductBase):
    min_stock_level: int = 0
    quantity: int = 1

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True