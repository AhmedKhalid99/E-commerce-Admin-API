from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product import ProductCreate
from fastapi import HTTPException

def create_product(db: Session, product: ProductCreate):
    try:
        existing_product = db.query(Product).filter(Product.sku == product.sku).first()
        if existing_product:
            raise HTTPException(status_code=400, detail=f"Product with SKU '{product.sku}' already exists.")

        db_product = Product(
            name=product.name,
            sku=product.sku,
            category=product.category,
            price=product.price,
        )
        db.add(db_product)
        db.flush()

        inventory = Inventory(
            product_id=db_product.id,
            quantity=product.quantity,
            min_stock_level=product.min_stock_level
        )
        db.add(inventory)

        db.commit()
        db.refresh(db_product)
        db.refresh(inventory)

        return db_product

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity Error: Invalid data.")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error occurred.")

def get_products(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Product).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database Error occurred.")
