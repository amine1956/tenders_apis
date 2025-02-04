import requests
from bs4 import BeautifulSoup

# Obtenez la réponse de la page
page = 0  # Remplacez par le numéro de page souhaité
tenders_response = requests.get(f'https://tenders.ppa.gov.gh/tenders?page={page}').text

# Analysez le contenu HTML
tenders_soup = BeautifulSoup(tenders_response, 'html.parser')

# Vérifiez la structure pour localiser la section souhaitée
data_container = tenders_soup.select_one('body > div:nth-of-type(1) > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')

if data_container:
    # Parcourez les données de la section pour extraire les informations
    tenders = []
    for tender in data_container.find_all('div', recursive=False):  # Ajustez selon la structure des éléments
        title = tender.find('div',class_='list-desc')  # Exemple pour trouver un titre
        date = tender.find('div', class_='list-date')  # Exemple pour trouver une date
        link = tender.find('a', href=True)  # Exemple pour trouver un lien
        agency = tender.find('div' , class_='list-agency')

        # Ajoutez les données extraites à une liste ou un dictionnaire
        tenders.append({
            'title': title.text.strip() if title else None,
            'date': date.text.strip() if date else None,
            'link': link['href'] if link else None,
            'agency': agency.text.strip() if agency else None,
        })

    # Affichez les données extraites
    for tender in tenders:
        print(tender)
else:
    print("Impossible de localiser la section des données.")


import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
import time

# --- MongoDB Setup ---
client = MongoClient("mongodb://localhost:27017/")
db = client["tenders_db"]
collection = db["tenders"]

# --- Base URL ---
base_url = "https://tenders.ppa.gov.gh/tenders"

# --- Function to extract tender links from a listing page ---
def get_tender_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    # Look for links that match the pattern /tenders/<number>
    for a in soup.find_all("a", href=True):
        href = a['href']
        if re.search(r"/tenders/\d+$", href):
            # Build full URL if needed
            full_url = href if href.startswith("http") else "https://tenders.ppa.gov.gh" + href
            links.append(full_url)
    return list(set(links))

# --- Function to parse the tender details page ---
def parse_tender_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Get all text using a separator that makes it easier to split by lines
    text = soup.get_text(separator='\n')
    # Normalize whitespace (remove extra newlines)
    text = re.sub(r'\n+', '\n', text)

    fields = {}
    # Define regex patterns for each field. Note that many fields are captured by matching the label and then
    # the rest of the line. For multi-line fields (like Tender Description), a more careful extraction is used.
    patterns = {
        'Tender Name': r"Tender Name:\s*(.*)",
        'Tender Type': r"Tender Type:\s*(.*)",
        'Package No': r"Package No:\s*(.*)",
        'Post Date': r"Post Date:\s*(.*)",
        'Closing Date': r"Closing Date:\s*(.*)",
        'Currency': r"Currency:\s*(.*)",
        'Price of Tender Document': r"Price of Tender Document:\s*(.*)",
        # Tender Description: capture from the label until we reach either LOTS DESCRIPTION or Additional Information
        'Tender Description': r"Tender Description:\s*((?:.|\n)*?)(?=\n(?:LOTS DESCRIPTION|Additional Information:))",
        # LOTS DESCRIPTION: capture from label until the next known label
        'LOTS DESCRIPTION': r"LOTS DESCRIPTION\s*((?:.|\n)*?)(?=\n(?:Additional Information:))",
        # Additional Information: capture until the next label (e.g. Email: or Source of Funds:)
        'Additional Information': r"Additional Information:\s*((?:.|\n)*?)(?=\n(?:Email:|Source of Funds:))",
        'Email': r"Email:\s*(.*)",
        'Source of Funds': r"Source of Funds:\s*(.*)",
        'No. of Lots': r"No\. of Lots:\s*(.*)",
        'Agency': r"Agency:\s*(.*)",
        'Region': r"Region:\s*(.*)",
        'District': r"District:\s*(.*)",
        'Contact Person': r"Contact Person:\s*(.*)",
        # For Telephone, allow both 'Tel' and 'Telephone'
        'Telephone': r"Tel(?:phone)?:\s*(.*)",
        'Fax': r"Fax:\s*(.*)",
        'Website': r"Website:\s*(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[key] = match.group(1).strip()
        else:
            fields[key] = None  # Field not found
    return fields

# --- Main Loop to iterate through listing pages and tender detail pages ---
page = 1
while True:
    print(f"Scraping listing page {page}...")
    params = {"page": page}  # Adjust this if the site uses a different pagination method
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print("Failed to retrieve listing page or reached end of listings.")
        break

    tender_links = get_tender_links(response.text)
    if not tender_links:
        print("No tender links found on page, ending loop.")
        break

    for tender_url in tender_links:
        print(f"Scraping tender details from {tender_url}...")
        detail_response = requests.get(tender_url)
        if detail_response.status_code != 200:
            print(f"Failed to retrieve tender details from {tender_url}")
            continue

        tender_details = parse_tender_details(detail_response.text)
        tender_details["url"] = tender_url  # Include the source URL
        # Insert the scraped data into MongoDB
        collection.insert_one(tender_details)
        print(f"Inserted tender: {tender_details.get('Tender Name')}")
        # Pause briefly to avoid overwhelming the server
        time.sleep(1)

    page += 1
    # Pause between pages
    time.sleep(2)
