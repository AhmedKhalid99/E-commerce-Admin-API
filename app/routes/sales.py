from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.controller import sales as crud_sales
from app.schemas import sales as schema_sales
from app.database import get_db

router = APIRouter()

@router.post("/order/create/", response_model=schema_sales.SalesOrder)
def create_order(
    order: schema_sales.SalesOrderCreate,
    db: Session = Depends(get_db)
):
    return crud_sales.create_sales_order(db, order)

@router.get("/orders/", response_model=list[schema_sales.SalesOrder])
def list_orders(
    db: Session = Depends(get_db)
):
    return crud_sales.get_all_orders(db)

@router.get("/order-items/{order_id}", response_model=schema_sales.SalesOrder)
def get_order_items(
    order_id: int,
    db: Session = Depends(get_db)
):
    return crud_sales.get_order_by_id(db, order_id)

@router.get("/revenue-summary", response_model=list[schema_sales.RevenueSummary])
def revenue_summary(
    group_by: str = Query("day"),
    db: Session = Depends(get_db)
):
    return crud_sales.get_revenue_summary(db, group_by=group_by)

@router.get("/compare-revenue_period", response_model=schema_sales.CompareRevenueByTimePeriod)
def compare_revenue_period(
    start1: str,
    end1: str,
    start2: str,
    end2: str,
    db: Session = Depends(get_db)
):
    return crud_sales.compare_revenue_period(db, start1, end1, start2, end2)

@router.get("/compare-revenue_categories", response_model=schema_sales.CompareRevenueByCategories)
def compare_revenue_categories(
    category1: str,
    category2: str,
    db: Session = Depends(get_db)
):
    return crud_sales.compare_revenue_categories(db, category1, category2)

@router.get("/compare-revenue/by-category-period", response_model=schema_sales.CompareRevenueByPeriodForCategory)
def compare_revenue_by_category_and_period(
    category: str,
    start1: str,
    end1: str,
    start2: str,
    end2: str,
    db: Session = Depends(get_db)
):
    return crud_sales.compare_revenue_by_category_and_period(db, category, start1, end1, start2, end2)

@router.get("/filter", response_model=list[schema_sales.SalesOrder])
def filter_sales_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    product_id: Optional[int] = None,
    category_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud_sales.get_filtered_sales_data(db, start_date, end_date, product_id, category_name)