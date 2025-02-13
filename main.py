from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from typing import List

app = FastAPI()

# Connexion à MongoDB (PORT 27017)
client = MongoClient("mongodb://localhost:27017")

db = client["tenders_db"]  # Remplace par le nom de ta base de données
collection = db["tenders"]  # Remplace par le nom de ta collection

@app.get("/")
def home():
    return {"message": "Bienvenue sur mon API FastAPI !"}


# 🔹 Route pour récupérer toutes les données
@app.get("/all_tenders", response_model=List[dict])
def get_all_data():
    data = list(collection.find({}, {"_id": 0}))  # Exclure l'ID MongoDB
    return data

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)