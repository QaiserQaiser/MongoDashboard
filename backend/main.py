from fastapi import FastAPI
from utils.db_connection import get_db
from lib.preprocess_orders import preprocess_orders
from lib.preprocess_customers import preprocess_customers
from lib.preprocess_products import preprocess_products
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    preprocess_orders(db)
    preprocess_customers(db)
    preprocess_products(db)
    yield
    print("Shutting down the application...")

# KPI: Orders per customer
@app.get("/kpi/orders-per-customer")
async def orders_per_customer():
    db = get_db()
    pipeline = [
        {"$group": {"_id": "$Customer ID", "total_orders": {"$sum": 1}}},
        {"$sort": {"total_orders": -1}},
    ]
    result = list(db.orders.aggregate(pipeline))
    return {"data": result}

