import requests 
import sys
from bs4 import BeautifulSoup
import csv

URL = 'https://www.nhsinform.scot/illnesses-and-conditions/a-to-z'

def get_content():
    response = requests.get(URL)
    properties = dir(response)
    if response.status_code == 200:
        return response
    else:
        print(f"Request failed. Maybe the server is down.")
        sys.exit()

def scrap_content():
    all_diagnosis = ()
    response = get_content()
    soup = BeautifulSoup(response.content, 'html.parser')
    s = soup.find('div', class_='row')
    ul_list =  soup.find_all('ul', class_='nhsuk-list')
    for ul in ul_list:
        link_elements = ul.find_all('a', class_='nhs-uk__az-link')
        for link in link_elements:
                text = link.get_text(strip=True)
                all_diagnosis += (text, )
    return all_diagnosis

def store_content(all_diagnosis):

    with open('diagnosis.csv', "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Diagnosis"])
        for value in all_diagnosis:
            writer.writerow([value])

if __name__ == '__main__':
    all_diagnosis = scrap_content()
    store_content(all_diagnosis)