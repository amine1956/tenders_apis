from fastapi import FastAPI
from routers import Get_tenders , insert_tenders

app = FastAPI()

app.include_router(Get_tenders.router)
app.include_router(insert_tenders.router) 

