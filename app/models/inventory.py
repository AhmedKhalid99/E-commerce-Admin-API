from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Float, nullable=False, default=0.0)
    min_stock_level = Column(Float, nullable=False, default=0.0)

    product = relationship("Product", back_populates="inventory")

class InventoryChange(Base):
    __tablename__ = "inventory_change"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    change_amount = Column(Float, nullable=False)
    name = Column(String(255), nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default= text('CURRENT_TIMESTAMP'))

    product = relationship("Product", back_populates="inventory_changes")
