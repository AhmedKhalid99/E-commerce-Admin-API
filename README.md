# E-commerce Admin API

This project provides an admin backend API for managing products, inventory, and sales orders using FastAPI and MySQL.

## ✅ Requirements

- Python 3.10+
- MySQL Server
- pip

---

## Setup Instructions

### 1. **Install Dependencies**
```bash
cd project directory
pip install -r requirements.txt
```

### 2. Update Environment Variables

Make sure your `.env` file contains the correct database credentials:
```
DB_USER= your-user
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=your-port
DB_NAME=your-db-name
```

### 3. **Seed the Database (MUST)**
- In order to create the tables and populate data run this command:

```bash
python3 app/seed_db.py
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API doc will be available at: [base-url:port/docs](http://localhost:8000/docs)

## API Endpoints

📁 Products
POST /products/create/ – Create Product

GET /products/ – Get Products

🧾 Sales
POST /sales/order/create/ – Create Order

GET /sales/orders/ – List Orders

GET /sales/order-items/{order_id} – Get Order Items

GET /sales/revenue-summary – Revenue Summary

GET /sales/compare-revenue_period – Compare Revenue Period

GET /sales/compare-revenue_categories – Compare Revenue Categories

GET /sales/compare-revenue/by-category-period – Compare Revenue By Category And Period

GET /sales/filter – Filter Sales Data

📦 Inventory
GET /inventory-management/ – Get Inventory List

GET /inventory-management/low-stock/ – Get Low Stock Alerts

POST /inventory-management/update/ – Update Inventory Level

GET /inventory-management/changes/ – Get Inventory Change History

🏠 Default
GET / – Read Root

## Notes
- Make sure MySQL is running and accessible.
- Replace database credentials in `.env file` as per your setup.
- Run the seed_db.py script.
