
import uvicorn
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import List

# Initialisation de l'application FastAPI
app = FastAPI()

# Connexion à MongoDB
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["tenders"]  # Collection "tenders"

@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}

@app.get("/tenders", response_model=List[dict])
def get_all_tenders():
    """Récupère tous les documents de la collection 'tenders'."""
    tenders = list(mycol.find({}, {"_id": 0}))  # Exclure `_id`
    return tenders

@app.get("/tenders/{tender_id}")
def get_tender_by_id(tender_id: str):
    """Récupère un document spécifique par son `_id`."""
    try:
        obj_id = ObjectId(tender_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    tender = mycol.find_one({"_id": obj_id})
    
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    tender["_id"] = str(tender["_id"])  # Convertir ObjectId en string
    return tender

uvicorn.run(app, port=8000, host= '127.0.0.1')