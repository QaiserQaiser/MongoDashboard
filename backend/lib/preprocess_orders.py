def preprocess_orders(db):
    """Preprocesses the orders collection."""
    orders_collection = db.orders

    orders = orders_collection.find()
    for order in orders:
        raw_data = order.get(
            "Row ID;Order ID;Order Date;Ship Date;Ship Mode;Customer ID;Segment;Postal Code;Product ID;Sales;Quantity;Discount;Profit"
        )
        if raw_data:
            field_data = raw_data.split(";")
            if len(field_data) == 13:
                updated_order = {
                    "Row ID": field_data[0],
                    "Order ID": field_data[1],
                    "Order Date": field_data[2],
                    "Ship Date": field_data[3],
                    "Ship Mode": field_data[4],
                    "Customer ID": field_data[5],
                    "Segment": field_data[6],
                    "Postal Code": field_data[7],
                    "Product ID": field_data[8],
                    "Sales": float(field_data[9]),
                    "Quantity": int(field_data[10]),
                    "Discount": float(field_data[11]),
                    "Profit": float(field_data[12]),
                }
                orders_collection.update_one({"_id": order["_id"]}, {"$set": updated_order})
