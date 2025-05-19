from sqlalchemy import Column, Integer, String, Float, DateTime, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False, unique=True)
    category = Column(String(255), nullable=False, default="default")
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    inventory = relationship("Inventory", uselist=False, back_populates="product")
    inventory_changes = relationship("InventoryChange", back_populates="product")
