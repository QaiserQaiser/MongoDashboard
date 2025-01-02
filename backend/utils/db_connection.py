from pymongo import MongoClient

def get_database():
    """Returns the connected MongoDB database instance."""
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["ecommerce"]
        return db
    except Exception as e:
        raise Exception(f"Database connection failed: {e}")
