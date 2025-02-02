from typing import Union
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import uvicorn 

app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"  # Replace with your MongoDB URI
DATABASE_NAME = "mynddatabase"  # Change to your database name

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db["tenders"]  # Change to your collection name

# Helper function to convert MongoDB document to JSON serializable format
def mongo_to_dict(mongo_obj):
    mongo_obj['_id'] = str(mongo_obj['_id'])  # Convert ObjectId to string
    return mongo_obj

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Create a new item
@app.post("/items/")
async def create_item(item: dict):
    result = await collection.insert_one(item)
    return {"inserted_id": str(result.inserted_id)}

# Get all items
@app.get("/items/all")
async def get_all_items():
    items = await collection.find().to_list(100)  # Get up to 100 items
    return {"items": [mongo_to_dict(item) for item in items]}  # Convert each item

# Get a specific item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return {"item": mongo_to_dict(item)}  # Convert the item
    else:
        return {"message": "Item not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    print(db.list_collection_names())
