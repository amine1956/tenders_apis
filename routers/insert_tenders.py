from fastapi import APIRouter
from pydantic import BaseModel
from tools.config_mongodb import  Mycol

class Tender(BaseModel) :
    _id : str | None = None
    title : str | None = None
    hyperlink : str  | None = None
    tender_name: str | None = None
    tender_type: str | None = None
    package_no: str | None = None
    post_date: str | None = None
    closing_date: str | None = None
    currency: str | None = None
    price_of_tender_document: str | None = None
    tender_description: str | None = None
    additional_information: str | None = None
    source_of_funds: str | None = None
    no_of_lots: str | None = None
    agency: str | None = None
    region: str | None = None
    district: str | None = None
    contact_person: str | None = None
    email: str | None = None
    telephone: str  | None = None
    fax: str | None = None
    website: str | None = None

router = APIRouter()  

@router.post('/insert')
def insert_tender(tender: Tender):
    tender_dict = tender.dict()
    result = Mycol.insert_one(tender_dict)
    return {"inserted_id": str(result.inserted_id)}     