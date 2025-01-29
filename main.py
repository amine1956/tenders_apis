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
