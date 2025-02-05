##from typing import Union
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import uvicorn 

app = FastAPI()

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mynddatabase"]
collection = db["tenders"]


def mongo_to_dict(mongo_obj):
    mongo_obj['_id'] = str(mongo_obj['_id'])  # Convert ObjectId to string
    return mongo_obj

@app.get("/")
async def read_root():
    return {"Runned app": "True"}

# Create a new item
@app.post("/items/")
async def create_item(item: dict):
    result = await collection.insert_one(item)
    return {"inserted_id": str(result.inserted_id)}


@app.get("/items/all")
async def get_all_items():
    items = await collection.find().to_list(None) 
    return {"items": [mongo_to_dict(item) for item in items]}  



@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return {"item": mongo_to_dict(item)}  # Convert the item
    else:
        return {"message": "Item not found"}


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(item_id)})

    if delete_result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

        
if __name__ == "__main__":
 uvicorn.run(app, host="127.0.0.1", port=8080)