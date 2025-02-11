
from fastapi import FastAPI,APIRouter,HTTPException
from typing import List
from tools.code_scrapping import collection


router=APIRouter()

@router.get("/tenders", response_model=List[dict])
def get_all_tenders():
    tenders = list(collection.find({}, {"_id": 0}))  
    if not tenders:
        raise HTTPException(status_code=404, detail="No tenders found")
    return tenders
#website to find all the data that we get from mongodb http://127.0.0.1:8000/tenders or http://127.0.0.1:8000/docs
