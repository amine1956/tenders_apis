from fastapi import APIRouter
from pydantic import BaseModel
from tools.config_mongodb import Mycol

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

@router.get('/tenders')
def get_tenders():
    documents = list(Mycol.find())
    Tenders = [Tender(  _id = str(document.get('_id')) ,
                        title = document.get('title') ,
                        hyperlink=document.get("hyperlink") ,
                        tender_name=document.get("Tender Name"),
                        tender_type=document.get("Tender Type") ,
                        package_no=document.get("Package No") ,
                        post_date=document.get("Post Date") ,
                        closing_date=document.get("Closing Date") ,
                        currency=document.get("Currency") ,
                        price_of_tender_document=document.get("Price of Tender Document") ,
                        tender_description=document.get("Tender Description") ,
                        additional_information=document.get("Additional information") ,
                        source_of_funds=document.get("Source of Funds") ,
                        no_of_lots=document.get("No.of Lots") ,
                        agency=document.get("Agency") ,
                        region=document.get("Region") ,
                        district=document.get("District") ,
                        contact_person=document.get("Contact Person") ,
                        email=document.get("Email") ,
                        telephone=document.get("Telephone") ,
                        fax=document.get("Fax") ,
                        website=document.get("Website") ,
                       )
               for document in documents]
    return Tenders   

