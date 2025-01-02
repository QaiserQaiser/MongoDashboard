from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']

@app.get("/kpi/orders-per-customer")
async def orders_per_customer():
    pipeline = [
        {"$group": {"_id": "$customer_id", "total_orders": {"$sum": 1}}},
        {"$sort": {"total_orders": -1}}
    ]
    result = list(db.orders.aggregate(pipeline))
    return {"data": result}
