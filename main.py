from fastapi import FastAPI
from routes.tenders import router as tenders_router

# 📌 Initialize FastAPI app
app = FastAPI()

# 📌 Include routes
app.include_router(tenders_router)

# 📌 Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
