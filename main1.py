from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

# 📌 Connexion à MongoDB
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["tenders_db"]
collection = db["tenders"]

app = FastAPI()

# 📌 Modèle pour valider les données des tenders
class Tender(BaseModel):
    title: str
    description: str
    budget: float
    date: str

### **1️⃣ CREATE - Ajouter un nouveau tender**
@app.post("/tenders/")
def create_tender(tender: Tender):
    new_tender = tender.dict()
    result = collection.insert_one(new_tender)
    return {"id": str(result.inserted_id), "message": "Tender ajouté avec succès !"}

### **2️⃣ READ - Récupérer tous les tenders**
@app.get("/tenders/")
def get_tenders():
    tenders = list(collection.find({}))
    
    if not tenders:
        raise HTTPException(status_code=404, detail="Aucun tender trouvé")

    # Convertir ObjectId en string
    for tender in tenders:
        tender["_id"] = str(tender["_id"])
    
    return tenders

### **3️⃣ READ - Récupérer un tender par ID**
@app.get("/tenders/{tender_id}")
def get_tender(tender_id: str):
    tender = collection.find_one({"_id": ObjectId(tender_id)})
    if not tender:
        raise HTTPException(status_code=404, detail="Tender non trouvé")

    tender["_id"] = str(tender["_id"])
    return tender

### **4️⃣ UPDATE - Modifier un tender par ID**
@app.put("/tenders/{tender_id}")
def update_tender(tender_id: str, updated_tender: Tender):
    result = collection.update_one(
        {"_id": ObjectId(tender_id)}, 
        {"$set": updated_tender.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tender non trouvé")

    return {"message": "Tender mis à jour avec succès !"}

### **5️⃣ DELETE - Supprimer un tender par ID**
@app.delete("/tenders/{tender_id}")
def delete_tender(tender_id: str):
    result = collection.delete_one({"_id": ObjectId(tender_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tender non trouvé")

    return {"message": "Tender supprimé avec succès !"}

# 📌 Démarrer le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
