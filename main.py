
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId

# 📌 Connexion à MongoDB
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["tenders_db"]
collection = db["tenders"]

app = FastAPI()

@app.get("/tenders/")
def get_tenders():
    tenders = list(collection.find({}))  # 🔹 Récupérer tous les champs

    # Vérifier si aucun document n'est trouvé
    if not tenders:
        raise HTTPException(status_code=404, detail="Aucun tender trouvé")

    # Convertir ObjectId en string pour éviter une erreur JSON
    for tender in tenders:
        tender["_id"] = str(tender["_id"])  # Convertir l'ObjectId en string
    
    return tenders  # Retourne tous les tenders avec leurs données complètes

# 📌 Démarrer le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

