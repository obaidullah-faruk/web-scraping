import requests 
import sys
from bs4 import BeautifulSoup
import csv
import string 


all_alphabets = list(string.ascii_lowercase)

BASE_URL = 'https://www.drugs.com/alpha/'

def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        print(f"Request failed. Maybe the server is down.")
        sys.exit() 


def scrap_content():
    all_medicines = ()
    for alphabet in all_alphabets:
        url = BASE_URL + alphabet + '.html'
        contents = get_content(url)
        soup = BeautifulSoup(contents.content, 'html.parser')
        soup_content = soup.find('div', id='content')
        soup_content_box = soup_content.find('div', class_='contentBox')
        soup_ul_items = soup_content_box.find('ul', class_='ddc-list-column-2')
        for li in soup_ul_items.find_all('li'):
            text = li.get_text(strip=True)
            all_medicines += (text, )
    return all_medicines


def store_content(medicines) -> None:

    with open('medicine.csv', "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Item Code"])
        for value in medicines:
            writer.writerow([value])


if __name__ == '__main__':
    medicines = scrap_content()
    store_content(medicines)
