from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller import inventory as crud_inventory
from app.schemas import inventory as schema_inventory
from typing import Optional

router = APIRouter()


@router.get("/", response_model=list[schema_inventory.InventoryStatus])
def get_inventory_list(db: Session = Depends(get_db)):
    return crud_inventory.get_inventory_status(db)


@router.get("/low-stock/", response_model=list[schema_inventory.InventoryStatus])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    return crud_inventory.get_low_stock_items(db)


@router.post("/update/", response_model=schema_inventory.InventoryChangeRead)
def update_inventory_level(
    update_data: schema_inventory.InventoryChangeCreate,
    db: Session = Depends(get_db)
):
    return crud_inventory.update_inventory(db, update_data)


@router.get("/changes/", response_model=list[schema_inventory.InventoryChangeRead])
def get_inventory_change_history(
    product_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)):
    return crud_inventory.get_inventory_changes(db, product_id=product_id, limit=limit)
