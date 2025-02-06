from fastapi import APIRouter
from tools.DataBase import collection

router=APIRouter()

@router.get('/tenders')
def get_tenders():
    documents = list(collection.find())
    return [{**document , "_id" : str(document["_id"])} for document in documents]
