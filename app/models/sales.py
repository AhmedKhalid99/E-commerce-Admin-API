from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class OrderStatusEnum(enum.Enum):
    pending = "pending"
    shipped = "shipped"
    completed = "completed"
    cancelled = "cancelled"
    refunded = "refunded"
    partially_refunded = "partially_refunded"

class ItemStatusEnum(enum.Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    refunded = "refunded"

class SalesOrder(Base):
    __tablename__ = "sales_order"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    customer_email = Column(String(255), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending)

    items = relationship("SalesOrderItem", back_populates="order", cascade="all, delete")

class SalesOrderItem(Base):
    __tablename__ = "sales_order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    category_name = Column(String(100), nullable=False, default="default")
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    item_status = Column(Enum(ItemStatusEnum), default=ItemStatusEnum.pending)

    order = relationship("SalesOrder", back_populates="items")
    product = relationship("Product")
