from fastapi import FastAPI
from tools.DataBase import collection
 
app = FastAPI()

@app.get('/tenders')
def get_tenders():
    documents = list(collection.find())
    return [{**document , "_id" : str(document["_id"])} for document in documents]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
#uvicorn main:app --reload
#http://127.0.0.1:8000/docs
