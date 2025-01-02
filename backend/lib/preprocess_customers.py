def preprocess_customers(db):
    """Preprocesses the customers collection."""
    customers_collection = db.customers

    customers = customers_collection.find()
    for customer in customers:
        raw_data = customer.get("Customer ID;Customer Name")
        if raw_data:
            field_data = raw_data.split(";")
            if len(field_data) == 2:
                updated_customer = {
                    "Customer ID": field_data[0],
                    "Customer Name": field_data[1],
                }
                customers_collection.update_one({"_id": customer["_id"]}, {"$set": updated_customer})
