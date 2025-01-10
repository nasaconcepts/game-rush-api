from pymongo import MongoClient
external_url = "mongodb+srv://chinasaobichere:6fC9ARDTkKaCfUPn@game-db-cluster.ra3y0.mongodb.net/?retryWrites=true&w=majority&appName=game-db-cluster"
local_url = "mongodb://localhost:27017/"
client = MongoClient(local_url)
db = client["gamedatabase"]  # Replace with your database name