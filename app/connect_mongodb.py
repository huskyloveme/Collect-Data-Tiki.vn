from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["project4"]
collection = db["products"]




