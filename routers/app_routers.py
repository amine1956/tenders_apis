from fastapi import APIRouter
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["wed_DB"]
collection = db['tenders']

router=APIRouter()
    
#Get all tenders
@router.get('/tenders')
def get_all_tenders():
    documents = list(collection.find())
    return [{**document , "_id" : str(document["_id"])} for document in documents]
