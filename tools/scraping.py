import requests 
from bs4 import BeautifulSoup
import pandas as pd 
from mongodb import insert_data 

link = requests.get("https://tenders.ppa.gov.gh/tenders?page=1")
soup = BeautifulSoup(link.text,'html.parser')
paragraph = soup.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div > p')
list_of_strings = paragraph.text.split() 
max_of_pages = int(list_of_strings[-1]) 

each_box_list = []
for i in range(1,(max_of_pages+1)) :  
    link = requests.get(f"https://tenders.ppa.gov.gh/tenders?page={i}") 
    soup = BeautifulSoup(link.text , 'html.parser')
    extracted_boxes = soup.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')
    list_boxes = extracted_boxes.find_all('div',class_='list-wrap') 
    for box in list_boxes : #with this i can get each box of all the pages in one list
        each_box_list.append(box) 
df_final_list = []                
for box in each_box_list :
    df_row_list = [] 
    title = box.find('div',class_='list-title') 
    df_row_list.append(title.text.strip())
    hyper_link = box.find('a',href=True)
    hyper_url = hyper_link['href']
    if hyper_url : 
        url = requests.get(hyper_url)
        soup_of_hl = BeautifulSoup(url.text , 'html.parser')
        extracted_hl_info = soup_of_hl.select_one('html > body > div > section:nth-of-type(2) > div > div > div > div > div:nth-of-type(2) > div')
        list_infos=extracted_hl_info.find_all('dd') 
        lista = []
        for info in list_infos : 
            lista.append(info.text.strip())    
    df_row_list.append(hyper_link['href']) 
    for information in lista : 
        df_row_list.append(information)
    df_final_list.append(df_row_list)    
        

cols = ['title','hyperlink','Tender Name','Tender Type','Package No','Post Date','Closing Date','Currency','Price of Tender Document','Tender Description','Additional information','Source of Funds','No.of Lots','Agency','Region','District','Contact Person','Email','Telephone','Fax','Website']

final_df = pd.DataFrame(df_final_list,columns=cols)  

insert_data(final_df=final_df)   