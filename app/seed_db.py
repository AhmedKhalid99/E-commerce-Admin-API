from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models.product import Product
from app.models.inventory import Inventory, InventoryChange
from app.models.sales import SalesOrder, SalesOrderItem, OrderStatusEnum, ItemStatusEnum

def seed_data():

    Base.metadata.create_all(bind=engine)  
    session = Session(bind=engine)

    if session.query(Product).first():
        print("Data already seeded, exiting.")
        session.close()
        return

    products = [
        Product(id=1, name="product1", sku="sku1", category="default1", price=10),
        Product(id=3, name="product2", sku="sku2", category="default1", price=100),
        Product(id=4, name="product3", sku="sku3", category="default1", price=110),
        Product(id=5, name="product4", sku="sku4", category="default", price=110),
        Product(id=6, name="product5", sku="sku5", category="default", price=110),
        Product(id=7, name="stringew", sku="sku9", category="default", price=110),
    ]
    session.add_all(products)
    session.commit()

    inventories = [
        Inventory(id=5, product_id=1, quantity=86, min_stock_level=5),
        Inventory(id=6, product_id=3, quantity=100, min_stock_level=20),
        Inventory(id=7, product_id=4, quantity=110, min_stock_level=15),
        Inventory(id=8, product_id=5, quantity=110, min_stock_level=15),
        Inventory(id=9, product_id=6, quantity=110, min_stock_level=290),
        Inventory(id=10, product_id=7, quantity=0, min_stock_level=35),
    ]
    session.add_all(inventories)
    session.commit()

    inventory_changes = [
        InventoryChange(id=1, product_id=1, change_amount=30, name="string334"),
        InventoryChange(id=2, product_id=1, change_amount=20, name="string334"),
        InventoryChange(id=3, product_id=1, change_amount=27, name="string334"),
        InventoryChange(id=4, product_id=1, change_amount=90, name="string334"),
    ]
    session.add_all(inventory_changes)
    session.commit()

    sales_orders = [
        SalesOrder(id=4, order_number="string1", customer_email="string@gmail.com", total_amount=20, status=OrderStatusEnum.pending),
        SalesOrder(id=5, order_number="string2", customer_email="string@gmail.com", total_amount=20, status=OrderStatusEnum.pending),
        SalesOrder(id=8, order_number="string3", customer_email="string@gmail.com", total_amount=200, status=OrderStatusEnum.pending),
        SalesOrder(id=9, order_number="string232", customer_email="string@gmail.com", total_amount=120, status=OrderStatusEnum.pending),
    ]
    session.add_all(sales_orders)
    session.commit()

    sales_order_items = [
        SalesOrderItem(id=1, order_id=4, product_id=1, quantity=2, price=10, total_price=20, item_status=ItemStatusEnum.pending, category_name="default"),
        SalesOrderItem(id=2, order_id=5, product_id=1, quantity=2, price=10, total_price=20, item_status=ItemStatusEnum.pending, category_name="default"),
        SalesOrderItem(id=5, order_id=8, product_id=3, quantity=5, price=40, total_price=200, item_status=ItemStatusEnum.pending, category_name="default1"),
        SalesOrderItem(id=6, order_id=9, product_id=1, quantity=4, price=30, total_price=120, item_status=ItemStatusEnum.pending, category_name="default"),
    ]
    session.add_all(sales_order_items)
    session.commit()

    session.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
