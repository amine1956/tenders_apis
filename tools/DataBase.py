from pymongo import MongoClient
from insert_service import df

client = MongoClient("mongodb://localhost:27017/")
db = client["wed_DB"]
collection = db['tenders']

# Step 3: Convert the DataFrame to a list of dictionaries
records = df.to_dict(orient='records')
# Step 4: Insert the records into MongoDB
collection.insert_many(records)

print(f"{len(records)} records Inserted into MongoDB!")
