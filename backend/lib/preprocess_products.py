def preprocess_products(db):
    """Preprocesses the products collection."""
    products_collection = db.products

    products = products_collection.find()
    for product in products:
        raw_data = product.get("Product ID;Category;Sub-Category;Product Name")
        if raw_data:
            field_data = raw_data.split(";")
            if len(field_data) == 4:
                updated_product = {
                    "Product ID": field_data[0],
                    "Category": field_data[1],
                    "Sub-Category": field_data[2],
                    "Product Name": field_data[3],
                }
                products_collection.update_one({"_id": product["_id"]}, {"$set": updated_product})
