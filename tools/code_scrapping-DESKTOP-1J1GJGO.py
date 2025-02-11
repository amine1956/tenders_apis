import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

link = requests.get('https://tenders.ppa.gov.gh/tenders?page=1')
soup = BeautifulSoup(link.text, 'html.parser')
extracted_elemnnt = soup.select_one('html>body>div>section:nth-of-type(2)>div>div>div>div>div:nth-of-type(2)>div>p')
pagination = extracted_elemnnt.text.split()
max = int(pagination[-1])
each_tender_list = []

for i in range(1, (max + 1)):
    link = requests.get(f"https://tenders.ppa.gov.gh/tenders?page={i}")
    body = soup.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')
    list_tenders = body.find_all('div', class_='list-wrap')
    for tender in list_tenders:
        each_tender_list.append(tender)

tenders_df = []

for tender in each_tender_list:
    info_list = []

    title = tender.find('div', class_='list-title')
    info_list.append(title.text if title else "")

    link = tender.find('a', href=True)
    h_l = link['href'] if link else ""
    if h_l:
        url = requests.get(h_l)
        soup_of_hl = BeautifulSoup(url.text, "html.parser")
        body = soup_of_hl.select_one('html>body>div>section:nth-of-type(2)>div>div>div>div>div:nth-of-type(2)>div')
        list_infos = body.find_all('dd')
        lista = [info.text.strip() for info in list_infos]
    else:
        lista = []

    info_list.append(h_l)
    info_list.extend(lista)

    agency = tender.find('div', class_='list-agency')
    info_list.append(agency.text.strip() if agency else "")

    description = tender.find('div', class_='list-desc')
    info_list.append(description.text if description else "")

    date = tender.find('div', class_='list-date')
    info_list.append(date.text.strip() if date else "")

    tenders_df.append(info_list)


columns = ['title', 'link', 'tender Name', 'Tender Type', 'Package No', 'Post Date', 'Closing Date', 'Currency',
           'Price of Tender Document', 'Tender Description', 'Additional Information', 'Source of Funds', 'No of Lots',
           'Agency', 'Region', 'District', 'Contact Person', 'Email', 'Telephone', 'Fax', 'Website', 'agency', 'description', 'date']

df = pd.DataFrame(tenders_df, columns=columns)
pd.set_option('display.max_columns', None)
print(df)



client = MongoClient("mongodb://localhost:27017")
db = client["tenders_db"]
collection = db["tenders_info"]



