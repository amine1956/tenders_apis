import uvicorn
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Dict
from pydantic import BaseModel

# Initialisation de l'application FastAPI
app = FastAPI()

# Connexion à MongoDB
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["tenders"]  # Collection "tenders"

# Modèle Pydantic pour la validation des données
class Tender(BaseModel):
    title: str
    description: str
    price: float

@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}

@app.get("/tenders", response_model=List[Dict])
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

@app.post("/tenders", response_model=Dict)
def create_tender(tender: Tender):
    """Crée un nouveau document dans la collection 'tenders'."""
    tender_dict = tender.dict()
    result = mycol.insert_one(tender_dict)
    tender_dict["_id"] = str(result.inserted_id)
    return tender_dict

@app.put("/tenders/{tender_id}", response_model=Dict)
def update_tender(tender_id: str, tender: Tender):
    """Met à jour un document existant."""
    try:
        obj_id = ObjectId(tender_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    update_result = mycol.update_one({"_id": obj_id}, {"$set": tender.dict()})
    
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    return {"message": "Tender updated successfully"}

@app.delete("/tenders/{tender_id}", response_model=Dict)
def delete_tender(tender_id: str):
    """Supprime un document spécifique."""
    try:
        obj_id = ObjectId(tender_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    delete_result = mycol.delete_one({"_id": obj_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    return {"message": "Tender deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
