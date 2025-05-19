from fastapi import FastAPI
from app.routes import products, sales, inventory
from app.database import Base, engine


# Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Admin API")

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory-management", tags=["Inventory"])  # Add this line

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}