from fastapi import FastAPI
from routers.app_routers import router

app = FastAPI()
#get data
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
#http://127.0.0.1:8000/docs
