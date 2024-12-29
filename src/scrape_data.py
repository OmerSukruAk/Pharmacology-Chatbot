import requests
import pandas as pd
from bs4 import BeautifulSoup

def send_request(url:str) -> str:
    response = requests.get(url)
    return response.text

def parse_drug_page(page_index:str) -> pd.DataFrame:
    
    soup = BeautifulSoup(page_index, 'html.parser')
    table_list = soup.find_all('ul', {'class': 'ddc-list-column-2'})

    data = []
    base_url = "https://www.drugs.com"
    for ul in table_list:
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            medicine_name = a_tag.text
            medicine_link = a_tag['href']
            data.append([medicine_name, base_url + medicine_link])

    df = pd.DataFrame(data, columns=['Medicine name', 'Medicine Link'])

    return df

def get_drug_from_letter(url:str,letter:str) -> pd.DataFrame:
    url = url + letter + ".html"

    page_index = send_request(url)
    df = parse_drug_page(page_index)
    
    return df

def get_all_drugs(url:str) -> pd.DataFrame:
    all_drugs = pd.DataFrame()
    for i in range(97, 123):
        letter = chr(i)
        all_drugs = pd.concat([all_drugs, get_drug_from_letter(url, letter)])
    
    return all_drugs

all_drugs = get_all_drugs(url = "https://www.drugs.com/alpha/")
all_drugs.to_csv("src/drugs/drug_files/all_drugs.csv", index=False)