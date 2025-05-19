from sqlalchemy.orm import Session
from app.models.sales import SalesOrder, SalesOrderItem
from app.models.inventory import Inventory 
from app.schemas.sales import SalesOrderCreate
from sqlalchemy import func
from typing import Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


def create_sales_order(db: Session, order: SalesOrderCreate):
    try:
        db_order = SalesOrder(
            order_number=order.order_number,
            customer_email=order.customer_email,
            total_amount=order.total_amount,
            status=order.status
        )
        db.add(db_order)
        db.flush()

        for item in order.items:
            inventory = db.query(Inventory).filter_by(product_id=item.product_id).first()
            if not inventory:
                raise HTTPException(status_code=404, detail=f"Inventory not found for product_id: {item.product_id}")
            if inventory.quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product_id {item.product_id}. Available: {inventory.quantity}, Requested: {item.quantity}"
                )

            inventory.quantity -= item.quantity

            db_item = SalesOrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                category_name=item.category_name,
                quantity=item.quantity,
                price=item.price,
                total_price=item.price * item.quantity,
                item_status=item.item_status,
            )
            db.add(db_item)

        db.commit()
        db.refresh(db_order)
        db.refresh(db_item)
        return db_order

    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity Error: duplicate or invalid product ID.")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error occurred.")


def get_all_orders(db: Session):
    try:
        return db.query(SalesOrder).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching all orders.")


def get_order_by_id(db: Session, order_id: int):
    try:
        order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching order by id.")


def get_revenue_summary(db: Session, group_by: str = "day"):
    try:
        format_str = {
            "day": "%Y-%m-%d",
            "week": "%Y-%u",
            "month": "%Y-%m",
            "year": "%Y"
        }.get(group_by, "%Y-%m-%d")

        results = db.query(
            func.date_format(SalesOrder.order_date, format_str).label("period"),
            func.sum(SalesOrder.total_amount).label("revenue")
        ).group_by("period").all()

        return [{"date": r.period, "revenue": float(r.revenue)} for r in results]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching revenue summary.")


def compare_revenue_period(db: Session, start1: str, end1: str, start2: str, end2: str):
    try:
        rev1 = db.query(func.sum(SalesOrder.total_amount)).filter(SalesOrder.order_date.between(start1, end1)).scalar() or 0
        rev2 = db.query(func.sum(SalesOrder.total_amount)).filter(SalesOrder.order_date.between(start2, end2)).scalar() or 0
        return {
            "period1": f"{start1} to {end1}",
            "revenue1": rev1,
            "period2": f"{start2} to {end2}",
            "revenue2": rev2
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while comparing revenue periods.")


def compare_revenue_categories(db: Session, category1: str, category2: str):
    try:
        rev1 = (
            db.query(func.sum(SalesOrderItem.total_price))
            .filter(SalesOrderItem.category_name == category1)
            .scalar()
            or 0
        )

        rev2 = (
            db.query(func.sum(SalesOrderItem.total_price))
            .filter(SalesOrderItem.category_name == category2)
            .scalar()
            or 0
        )

        return {
            "Category1": category1,
            "revenue1": rev1,
            "Category2": category2,
            "revenue2": rev2,
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while comparing revenue categories.")


def compare_revenue_by_category_and_period(
    db: Session,
    category: str,
    start1: str,
    end1: str,
    start2: str,
    end2: str
):
    try:
        revenue1 = (
            db.query(func.sum(SalesOrderItem.total_price))
            .join(SalesOrder)
            .filter(
                SalesOrderItem.category_name == category,
                SalesOrder.order_date.between(start1, end1)
            )
            .scalar() or 0
        )

        revenue2 = (
            db.query(func.sum(SalesOrderItem.total_price))
            .join(SalesOrder)
            .filter(
                SalesOrderItem.category_name == category,
                SalesOrder.order_date.between(start2, end2)
            )
            .scalar() or 0
        )

        return {
            "category": category,
            "period1": f"{start1} to {end1}",
            "revenue1": revenue1,
            "period2": f"{start2} to {end2}",
            "revenue2": revenue2
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while comparing revenue by category and period.")


def get_filtered_sales_data(
    db: Session,
    start_date: Optional[str],
    end_date: Optional[str],
    product_id: Optional[int],
    category_name: Optional[str]
) -> list[SalesOrder]:
    try:
        query = db.query(SalesOrder)

        if product_id or category_name:
            query = query.join(SalesOrderItem)

        if start_date and end_date:
            query = query.filter(SalesOrder.order_date.between(start_date, end_date))
        elif start_date:
            query = query.filter(SalesOrder.order_date >= start_date)
        elif end_date:
            query = query.filter(SalesOrder.order_date <= end_date)

        if product_id:
            query = query.filter(SalesOrderItem.product_id == product_id)

        if category_name:
            query = query.filter(SalesOrderItem.category_name == category_name)

        return query.all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while fetching filtered sales data.")
