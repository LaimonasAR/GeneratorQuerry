"""
    Get all electronic items monetary value made 1 years, 2 months and 12 days from today.
    Get average price for all items/categories in the store.
    Get all items which names starts with letter a, and cost is between 10 and 100.
    Find all item names (only) for prices > 50 and quantity < 10.
"""

from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import timedelta, date

client = MongoClient("mongodb://0.0.0.0:27017/")
db = client["Store"]
collection = db["Items"]

def filter_documents(
    collection: Collection, field_name: str, eq_value: str
) -> List[dict]:
    query = {field_name: {"$eq": eq_value}}
    result = collection.find(query)
    return list(result)


def filter_documents_by_price_range(
    collection: Collection, field_name: str, gt_value: int, lt_value: int
) -> List[dict]:
    query = {field_name: {"$gt": gt_value, "$lt": lt_value}}
    result = collection.find(query)
    return list(result)


def filter_documents_by_price(
    collection: Collection, field_name: str, gt_value: int
) -> List[dict]:
    query = {field_name: {"$gt": gt_value}}
    result = collection.find(query)
    return list(result)

def get_electronics():
    my_filter = filter_documents(
        collection=collection, field_name="Category", eq_value="Electronics"
    )

    today = date.today()
    duration = timedelta(days=437)
    my_date = today - duration
    date_iso = my_date.isoformat()

    for item in my_filter:
        result = {}
        if item["Year made"] < date_iso:
            # print(item["Name"], item["Price"])
            result[item["Name"]] = item["Price"]

        print(result)


def Get_average_price():
    my_filter = filter_documents(
        collection=collection, field_name="Category", eq_value="Electronics"
    )

    amount = len(my_filter)
    result = 0
    for items in my_filter:
        result += items["Price"]
    average = round((result / amount), 2)

    print(f"Electronics - {average}")

    my_filter = filter_documents(
        collection=collection, field_name="Category", eq_value="Fruit"
    )

    amount = len(my_filter)
    result = 0
    for items in my_filter:
        result += items["Price"]
    average = round((result / amount), 2)

    print(f"Fruit - {average}")

    my_filter = filter_documents(
        collection=collection, field_name="Category", eq_value="Food"
    )

    amount = len(my_filter)
    result = 0
    for items in my_filter:
        result += items["Price"]
    average = round((result / amount), 2)

    print(f"Food - {average}")


def get_items_in_price_range():
    my_filter = filter_documents_by_price_range(
        collection=collection, field_name="Price", gt_value=10, lt_value=100
    )
    for item in my_filter:
        if item["Name"].startswith("c"):
            print(item)

def get_items_by_price_and_quantity():
    my_filter = filter_documents_by_price(
        collection=collection, field_name="Price", gt_value=50
    )
    item_list = []
    for item in my_filter:
        if item["Quantity"] < 10:
            item_list.append(item["Name"])
    print(item_list)