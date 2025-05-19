from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SalesOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float
    category_name: Optional[str] = "default"  
    item_status: Optional[str] = "pending"

class SalesOrderItemCreate(SalesOrderItemBase):
    pass

class SalesOrderItem(SalesOrderItemBase):
    id: int
    total_price: float

    class Config:
        from_attributes = True

class SalesOrderBase(BaseModel):
    order_number: str
    customer_email: str
    total_amount: float
    status: Optional[str] = "pending"

class SalesOrderCreate(SalesOrderBase):
    items: List[SalesOrderItemCreate]

class SalesOrder(SalesOrderBase):
    id: int
    order_date: datetime
    items: List[SalesOrderItem]

    class Config:
        from_attributes = True

class RevenueSummary(BaseModel):
    date: str
    revenue: float

class CompareRevenueByTimePeriod(BaseModel):
    period1: str
    revenue1: float
    period2: str
    revenue2: float

class CompareRevenueByCategories(BaseModel):
    Category1: str
    revenue1: float
    Category2: str
    revenue2: float

class CompareRevenueByPeriodForCategory(CompareRevenueByTimePeriod):
    category: str

