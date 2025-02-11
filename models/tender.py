from pydantic import BaseModel

# 📌 Define Tender model
class Tender(BaseModel):
    title: str
    description: str
    budget: float
    date: str
