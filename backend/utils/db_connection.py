from pymongo import MongoClient

def get_db():
    """Returns the connected MongoDB database instance."""
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["ecommerce"]
        return db
    except Exception as e:
        raise Exception(f"Database connection failed: {e}")
