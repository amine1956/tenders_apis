from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# Initialize a list to collect tender data from all pages
all_tenders = []

# Iterate through the pages (in this case, 1 to 3 inclusive)
for page in range(1, 4):  # Pages 1, 2, and 3
    print(f"Scraping page {page}...")
    # Get the response for the page
    tenders_response = requests.get(f'https://tenders.ppa.gov.gh/tenders?page={page}').text

    # Parse the HTML content
    tenders_soup = BeautifulSoup(tenders_response, 'html.parser')

    # Check the structure to locate the desired section
    data_container = tenders_soup.select_one('body > div:nth-of-type(1) > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')

    if data_container:
        # Loop through the section data to extract information
        for tender in data_container.find_all('div', recursive=False):  # Adjust according to element structure
            link = tender.find('a', href=True)  # Example to find a link

            # Add the extracted data to a list or dictionary
            if link:
                tender_url = link['href']
                # Access each link and scrape the data
                tender_response = requests.get(tender_url).text
                tender_soup = BeautifulSoup(tender_response, 'html.parser')

                # Example: Adjust according to the internal structure of the tender's pages
                tender_content = tender_soup.select_one('body > div > section.main-content.bg-sidebar.sidebar-left.mr-b-50 > div > div > div > div > div.col-md-9 > div')

                # Save the data in a list of dictionaries
                all_tenders.append({
                    'link': tender_url,
                    'content': tender_content.text.strip() if tender_content else None,
                })
    else:
        print(f"Unable to locate data section on page {page}.")

# Insert all extracted data into MongoDB
try:
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['data_ghana']  # Database name
    collection = db['all_tenders']  # Collection name

    # Insert data
    if all_tenders:
        result = collection.insert_many(all_tenders)
        print(f"{len(result.inserted_ids)} documents inserted into MongoDB!")
    else:
        print("No data to insert.")
except Exception as e:
    print("MongoDB Error:", e)