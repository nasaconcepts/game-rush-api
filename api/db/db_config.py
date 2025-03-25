from pymongo import MongoClient
import os

external_url = "mongodb+srv://chinasaobichere:6fC9ARDTkKaCfUPn@game-db-cluster.ra3y0.mongodb.net/?retryWrites=true&w=majority&appName=game-db-cluster"
local_url = os.getenv("MONGO_DATABASE_URL")
db_name= os.getenv("MONGO_DATABASE_NAME")
client = MongoClient(local_url)
db = client[db_name]  # Replace with your database name