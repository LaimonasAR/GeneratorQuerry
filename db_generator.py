"""

Task Nr.1 : Create the CLI application, that would populate MongoDB database with random data. The input should ask for :

    database name
    collection name
    field name with types (string, number, date string objects etc.) with range of values (lets say field name = price , 
    then value is number (float, int) which is random number from a(min) to b(max) )
    number o documents to create.

"""
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Any
from random import randint
from py_random_words import RandomWords
import random
from datetime import date, timedelta

def get_databasse_name() -> str:
    return input("Enter db name: ")

def get_collection_name() -> str:
    return input("Enter collection name: ")

def get_field_name() -> str:
    return input("Enter field name: ")

def get_field_value_type() -> str:
    return input("Enter field value type: ")

def get_range_min() -> int:
    return int(input("Enter a minimum value: "))

def get_range_max() -> int:
    return int(input("Enter a maximum value: "))

def get_number_of_docs() -> int:
    return int(input("Enter number of documents: "))

def get_number_of_fields():
    return int(input("enter number of fields"))

def get_range_min_float() -> float:
    return int(input("Enter a minimum value: "))

def get_range_max_float() -> float:
    return int(input("Enter a maximum value: "))



class DbGenerator:
    def __init__(self, host: str, port: int, db_name: str, coll: str) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name
        self.coll = coll

    def connect_to_mongodb(self) -> Database:
        client = MongoClient(self.host, self.port)
        database = client[self.db_name]
        return database

    def find_task(self, query: dict) -> List[Dict]:
        db = self.connect_to_mongodb()
        collection = db[self.coll]
        tasks = collection.find(query)
        return list(tasks)

    def create_task(self, document: dict) -> str:
        db = self.connect_to_mongodb()
        collection = db[self.coll]
        result = collection.insert_one(document)
        return f"Inserted document with ID: {result.inserted_id}"

    def update_task(self, query: Dict, update: Dict) -> int:
        db = self.connect_to_mongodb()
        collection = db[self.coll]
        result = collection.update_many(query, {"$set": update})
        return f"Modified {result.modified_count} tasks"

    def delete_tasks(self, query: Dict) -> int:
        db = self.connect_to_mongodb()
        collection = db[self.coll]
        result = collection.delete_many(query)
        return f"Deleted {result.deleted_count} tasks"
    
    def get_single_query(self, query: Dict[str, Any], fields: Dict[str, Any]):
        db = self.connect_to_mongodb()
        collection = db[self.coll]
        result = collection.find_one(query, fields)
        return result

def generate_random_date():
    start_date = "2000-01-01"
    end_date = "2023-12-31"

    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    delta = (end_date - start_date).days
    random_days = random.randint(0, delta)
    random_date = start_date + timedelta(days=random_days)
    return random_date.isoformat()

def generate_random_float(start_number, end_number):
    random_float = random.uniform(start_number, end_number)
    random_float = round(random_float, 2)
    return random_float

def get_random_category():
    string_list = ["Electronics", "Fruit", "Food"]
    random_string = random.choice(string_list)
    return random_string

def get_value():
    field_name = get_field_name()
    field_type = get_field_value_type()
    if field_type == "int":
        min= get_range_min()
        max = get_range_max()
        field_value = [min, max]
    if field_type == "str":
        field_value = ""
    if field_type == "float":
        min= get_range_min_float()
        max = get_range_max_float()
        field_value = [min, max]
    if field_type == "date":
        field_value = ""
    if field_type == "category":
        field_value = ""
    return [field_name, field_type, field_value]
    
def build_value_list():
    field_list = []
    add = True
    while add:
        print("Do You want to add a field? ")
        cont = input("Y, N?")
        if cont =="N":
            add = False
            break
        else:
            field = get_value()
            field_list.append(field)
    return field_list


def generate_doc(value_list, task_creator):

    value_dict = {}
    for value in value_list:
        if value[1] == "int":
            value_dict[value[0]] = randint(value[2][0],value[2][1])
        if value[1] == "str":
            ran_str = RandomWords()
            value_dict[value[0]] = ran_str.get_word()
        if value[1] == "float":
            value_dict[value[0]] = generate_random_float(value[2][0],value[2][1])
        if value[1] == "date":
            ran_date = generate_random_date()
            value_dict[value[0]] = ran_date
        if value[1] == "category":
            ran_category = get_random_category()
            value_dict[value[0]] = ran_category
    task_creator.create_task(document=value_dict)
    
def app():
    task_creator = DbGenerator(host="0.0.0.0", port = 27017, db_name=get_databasse_name(), coll= get_collection_name())
    value_list = build_value_list()
    how_many = int(input("How many documents would You like to create: "))
    for i in range(0, how_many):
        generate_doc(value_list, task_creator)
    
app()

