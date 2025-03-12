from fastapi import APIRouter,Request
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi.templating import Jinja2Templates


router=APIRouter()

client = AsyncIOMotorClient("mongodb://mongo-container:27017/")
db = client["mynddatabase"]
collection = db["tenders"]

templates = Jinja2Templates(directory="templates")

def id_to_string(mongo_objs):
    for mongo_obj in mongo_objs:
     mongo_obj['_id'] = str(mongo_obj['_id'])
    return mongo_objs

@router.get("/")
async def read_root():
    return {"Runned app": "True"}

@router.post("/items/")
async def create_item(item: dict):
    result = await collection.insert_one(item)
    return {"inserted_id": str(result.inserted_id)}


@router.get("/items/all")
async def get_all_items():
    items = await collection.find().to_list(None) 
    return {"items": id_to_string(items)}  


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(item_id)})

    if delete_result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    else:
        return {"result":"fatal error #####"}

@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})