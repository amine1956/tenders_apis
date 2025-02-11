from pymongo import MongoClient

# 📌 Connect to MongoDB
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["tenders_db"]
collection = db["tenders"]
