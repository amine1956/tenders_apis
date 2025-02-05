from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# ouvrir une liste pour stocker les donnes
all_tenders = []

# boucler sur 3 pages
for page in range(1, 4):  # Pages 1, 2, and 3
    print(f"Scraping page {page}...")
    # Get the response for the page
    tenders_response = requests.get(f'https://tenders.ppa.gov.gh/tenders?page={page}').text

    # Analyse du contenu HTML avec BeautifulSoup
    tenders_soup = BeautifulSoup(tenders_response, 'html.parser')

    # Check the structure to locate the desired section
    data_container = tenders_soup.select_one('body > div:nth-of-type(1) > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')

    if data_container:
        # loop pour trouver les liens
        for tender in data_container.find_all('div', recursive=False):  # Adjust according to element structure
            link = tender.find('a', href=True)  # Example to find a link

            # Add the extracted data to a list or dictionary
            if link:
                tender_url = link['href']
                # Access each link and scrape the data
                tender_response = requests.get(tender_url).text
                tender_soup = BeautifulSoup(tender_response, 'html.parser')

                # Scraping content under the 'dd' tags
                dd_tags = tender_soup.find_all('dd')
                dd_content = [dd.text.strip() for dd in dd_tags]

                # Define variables based on dd_content
                if len(dd_content) >= 19:  # Ensure sufficient data to map variables
                    Tender_Name = dd_content[0]
                    Tender_Type = dd_content[1]
                    Package_No = dd_content[2]
                    Post_Date = dd_content[3]
                    Closing_Date = dd_content[4]
                    Currency = dd_content[5]
                    Price_Document = dd_content[6]
                    Tender_Description = dd_content[7]
                    Additional_Information = dd_content[8]
                    Source_of_Funds = dd_content[9]
                    No_of_Lots = dd_content[10]
                    Agency = dd_content[11]
                    Region = dd_content[12]
                    District = dd_content[13]
                    Contact_Person = dd_content[14]
                    Email = dd_content[15]
                    Phone = dd_content[16]
                    Fax = dd_content[17]
                    website = dd_content[18]

                # Save the data in a list of dictionaries
                all_tenders.append({
                    'link': tender_url,
                    'Tender_Name': Tender_Name if len(dd_content) >= 1 else None,
                    'Tender_Type': Tender_Type if len(dd_content) >= 2 else None,
                    'Package_No': Package_No if len(dd_content) >= 3 else None,
                    'Post_Date': Post_Date if len(dd_content) >= 4 else None,
                    'Closing_Date': Closing_Date if len(dd_content) >= 5 else None,
                    'Currency': Currency if len(dd_content) >= 6 else None,
                    'Price_Document': Price_Document if len(dd_content) >= 7 else None,
                    'Tender_description': Tender_Description if len(dd_content) >= 8 else None,
                    'Additional_Information': Additional_Information if len(dd_content) >= 9 else None,
                    'Source_of_Funds': Source_of_Funds if len(dd_content) >= 10 else None,
                    'No_of_Lots': No_of_Lots if len(dd_content) >= 11 else None,
                    'Agency': Agency if len(dd_content) >= 12 else None,
                    'Region': Region if len(dd_content) >= 13 else None,
                    'District': District if len(dd_content) >= 14 else None,
                    'Contact_Person': Contact_Person if len(dd_content) >= 15 else None,
                    'Email': Email if len(dd_content) >= 16 else None,
                    'Phone': Phone if len(dd_content) >= 17 else None,
                    'Fax': Fax if len(dd_content) >= 18 else None,
                    'website': website if len(dd_content) >= 19 else None


                })

    else:
        print(f"Unable to locate data section on page {page}.")

# Insert all extracted data into MongoDB
try:
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27018/')
    db = client['data_tender']  # Database name
    collection = db['all_tenders']  # Collection name

    # Insert data
    if all_tenders:
        result = collection.insert_many(all_tenders)
        print(f"{len(result.inserted_ids)} documents inserted into MongoDB!")
    else:
        print("No data to insert.")
except Exception as e:
    print("MongoDB Error:", e)


from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from typing import List

app = FastAPI()

# Connexion à MongoDB (PORT 27018)
client = MongoClient("mongodb://localhost:27018")

db = client["data_tender"]  # Remplace par le nom de ta base de données
collection = db["all_tenders"]  # Remplace par le nom de ta collection

@app.get("/")
def home():
    return {"message": "Bienvenue sur mon API FastAPI !"}


# 🔹 Route pour récupérer toutes les données
@app.get("/all_tenders", response_model=List[dict])
def get_all_data():
    data = list(collection.find({}, {"_id": 0}))  # Exclure l'ID MongoDB
    return data
