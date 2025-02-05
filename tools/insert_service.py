from bs4 import BeautifulSoup
import requests
import pandas as pd
from data import add_info

#getting all the data from the webpage and parsing it with BeautifulSoup
link = requests.get("https://tenders.ppa.gov.gh/tenders?page=1")
soup=BeautifulSoup(link.text , "html.parser")
#put into paragraph the link to the text when it contain the number of the page : /html/body/div/section[2]/div/div/div/div/div[2]/div/p
page_number_button = soup.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div > p')
list_of_strings = page_number_button.text.split() #--> ['Showing', 'Page', '1', 'of', '3']
max= int(list_of_strings[-1]) # max = 3 in this case
each_box_list = []
for i in range(1,(max+1)) :  
    link = requests.get(f"https://tenders.ppa.gov.gh/tenders?page={i}")  #with this i can get each box of all the pages in one list
    soup = BeautifulSoup(link.text , 'html.parser')
    extracted_boxes = soup.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')
    list_boxes = extracted_boxes.find_all('div',class_='list-wrap') 
    for box in list_boxes : 
        each_box_list.append(box)

#df_list is the final table that contains all the data we scraped
df_list = []
#looping through every single tender and extracting all the data it contains
for box in each_box_list : 
    tender = []
    '''title'''
    title = box.find('div',class_='list-title')
    tender.append(title.text)
    #extracting the HTML code of the link in each tender, placing it in the 'link' variable, and then extracting just the URL and storing it in the 'hyper_link' variable
    link = box.find('a',href=True)# <a href="https://tenders.ppa.gov.gh/tenders/31734">tender title</a>
    hyper_link=link['href']# 'https://tenders.ppa.gov.gh/tenders/31734'
    #here is the part where we access the hyper link infos if a hyper_link exists
    if hyper_link :
        url = requests.get(hyper_link)
        soup_of_hl = BeautifulSoup(url.text , 'html.parser')
        #getting all the tender data
        extracted_hl_info = soup_of_hl.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')
        dl_elements=extracted_hl_info.find_all('dl')
        
        #extracting and placing each piece of information in the info_list
        info_list=[]
        for dl in dl_elements:
            dd = dl.find('dd').text.strip() if dl.find('dd') else ''
            info_list.append(dd)
    '''hyper_link'''         
    tender.append(hyper_link)
    #calling the add_info function from the data file, which contains all the processes for getting and appending data to the tender list      
    add_info(info_list,tender) 

    df_list.append(tender) 
columns = ['title', 'link', 'type', 'package number', 'post date', 'closing date', 'currency', 'price', 'description', 'additional info', 'source of funds', 'number of lots', 'agency', 'region', 'district', 'contact person', 'email', 'telephone', 'fax', 'website']
df = pd.DataFrame(df_list , columns=columns)
