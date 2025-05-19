from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controller import product as crud_product
from app.schemas import product as schema_product
from app.database import get_db

router = APIRouter()

@router.post("/create/", response_model=schema_product.Product)
def create_product(product: schema_product.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product)

@router.get("/", response_model=list[schema_product.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip=skip, limit=limit)
