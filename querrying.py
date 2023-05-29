from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import timedelta
#from db_generator import DbGenerator

# connection = DbGenerator(host="0.0.0.0", port = 27017, db_name="Grocerie_Store", coll= "Groceries")
# db = connection.connect_to_mongodb()

client = MongoClient("mongodb://0.0.0.0:27017/")
db = client["Store"]
collection = db["Items"]

#collection = DbGenerator(host="0.0.0.0", port = 27017, db_name="Store", coll= "Items")

def filter_documents(collection: Collection, field_name: str, eq_value: str, ne_value: str) -> List[dict]:
    """
    Filters documents in a MongoDB collection based on field values using $eq and $ne operators.

    Args:
        collection: The MongoDB collection to filter.
        field_name: The name of the field to filter.
        eq_value: The equal value to match.
        ne_value: The not equal value to exclude.

    Returns:
        A list of documents that match the filter criteria.
    """
    query = {
        field_name: {
            "$eq": eq_value,
            "$ne": ne_value
        }
    }
    result = collection.find(query)
    return list(result)

print(filter_documents(collection=collection, field_name="Category", eq_value="Food", ne_value="Fish"))

