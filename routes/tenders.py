from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.tender import Tender
from database import collection

# 📌 Create a router
router = APIRouter()

# **1️⃣ CREATE - Add a new tender**
@router.post("/tenders/")
def create_tender(tender: Tender):
    new_tender = tender.dict()
    result = collection.insert_one(new_tender)
    return {"id": str(result.inserted_id), "message": "Tender ajouté avec succès !"}

# **2️⃣ READ - Get all tenders**
@router.get("/tenders/")
def get_tenders():
    tenders = list(collection.find({}))

    if not tenders:
        raise HTTPException(status_code=404, detail="Aucun tender trouvé")

    # Convert ObjectId to string
    for tender in tenders:
        tender["_id"] = str(tender["_id"])

    return tenders

# **3️⃣ READ - Get a tender by ID**
@router.get("/tenders/{tender_id}")
def get_tender(tender_id: str):
    tender = collection.find_one({"_id": ObjectId(tender_id)})
    if not tender:
        raise HTTPException(status_code=404, detail="Tender non trouvé")

    tender["_id"] = str(tender["_id"])
    return tender

# **4️⃣ UPDATE - Modify a tender by ID**
@router.put("/tenders/{tender_id}")
def update_tender(tender_id: str, updated_tender: Tender):
    result = collection.update_one(
        {"_id": ObjectId(tender_id)}, 
        {"$set": updated_tender.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tender non trouvé")

    return {"message": "Tender mis à jour avec succès !"}

# **5️⃣ DELETE - Delete a tender by ID**
@router.delete("/tenders/{tender_id}")
def delete_tender(tender_id: str):
    result = collection.delete_one({"_id": ObjectId(tender_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tender non trouvé")

    return {"message": "Tender supprimé avec succès !"}
