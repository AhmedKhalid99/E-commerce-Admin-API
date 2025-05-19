from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.inventory import Inventory, InventoryChange
from app.models.product import Product
from app.schemas.inventory import InventoryChangeCreate
from fastapi import HTTPException


def get_inventory_status(db: Session):
    try:
        result = (
            db.query(Inventory, Product.name)
            .join(Product, Product.id == Inventory.product_id)
            .all()
        )
        return [
            {
                "product_id": inv.product_id,
                "product_name": name,
                "quantity": inv.quantity,
                "min_stock_level": inv.min_stock_level,
            }
            for inv, name in result
        ]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching inventory status.")


def get_low_stock_items(db: Session):
    try:
        result = (
            db.query(Inventory, Product.name)
            .join(Product, Product.id == Inventory.product_id)
            .filter(Inventory.quantity < Inventory.min_stock_level)
            .all()
        )
        return [
            {
                "product_id": inv.product_id,
                "product_name": name,
                "quantity": inv.quantity,
                "min_stock_level": inv.min_stock_level,
            }
            for inv, name in result
        ]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching low stock items.")


def update_inventory(db: Session, data: InventoryChangeCreate):
    try:
        inventory = db.query(Inventory).filter_by(product_id=data.product_id).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory record not found")

        inventory.quantity = data.change_amount

        change_record = InventoryChange(
            product_id=data.product_id,
            change_amount=data.change_amount,
            name=data.name
        )
        db.add(change_record)
        db.commit()
        db.refresh(change_record)

        return change_record
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while updating inventory.")


def get_inventory_changes(db: Session, product_id: int | None = None, limit: int = 100):
    try:
        query = db.query(InventoryChange).order_by(InventoryChange.changed_at.desc())
        
        if product_id is not None:
            query = query.filter(InventoryChange.product_id == product_id)
        
        return query.limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching inventory changes.")
