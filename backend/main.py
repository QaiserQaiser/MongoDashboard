from fastapi import FastAPI, HTTPException
from pymongo import MongoClient, errors
from fastapi.responses import JSONResponse

app = FastAPI()

# Initialize MongoDB client
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    # Test MongoDB connection
    client.admin.command('ping')
    db = client['ecommerce']
except errors.ServerSelectionTimeoutError:
    raise HTTPException(status_code=500, detail="Unable to connect to the MongoDB server")


@app.get("/kpi/orders-per-customer", response_class=JSONResponse)
async def orders_per_customer():
    try:
        # Define the aggregation pipeline
        pipeline = [
            # Extract Customer ID from the semicolon-separated string
            {
                "$addFields": {
                    "Customer ID": {
                        "$arrayElemAt": [
                            {"$split": ["$Row ID;Order ID;Order Date;Ship Date;Customer ID;Segment;Postal Code;Product ID;Sales;Quantity;Discount;Profit", ";"]},
                            4
                        ]
                    }
                }
            },
            # Match non-null Customer IDs
            {"$match": {"Customer ID": {"$ne": None}}},
            # Group by Customer ID
            {"$group": {"_id": "$Customer ID", "total_orders": {"$sum": 1}}},
            # Join with the customers collection for additional details
            {
                "$lookup": {
                    "from": "customers",
                    "localField": "_id",
                    "foreignField": "Customer ID",
                    "as": "customer_details"
                }
            },
            # Unwind customer details
            {"$unwind": {"path": "$customer_details", "preserveNullAndEmptyArrays": True}},
            # Sort by total orders in descending order
            {"$sort": {"total_orders": -1}}
        ]

        
        # Execute the aggregation
        result = list(db.orders.aggregate(pipeline))

        # Format response to include customer details
        formatted_result = [
            {
                "customer_id": doc["_id"],
                "total_orders": doc["total_orders"],
                "customer_name": doc.get("customer_details", {}).get("Customer Name", "Unknown")
            }
            for doc in result
        ]

        return {"data": formatted_result}
    except errors.PyMongoError as e:
        # Handle any MongoDB-related errors
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")
    except Exception as e:
        # Catch all other exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
