import requests
from bs4 import BeautifulSoup
import json
import os

PARAMS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def chek_directory():
    folder_name = f"data"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
        os.mkdir(folder_name)


def collection_links_festivals():
    fests_urls_list = []
    for i in range(0, 168, 24):
        url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=20%20Jul%202022&to_date=&maxprice=500&o={i}&bannertitle=July"

        req = requests.get(url=url, headers=PARAMS)
        json_data = json.loads(req.text)
        html_response = json_data["html"]

        with open(f"data/index_{i}.html", "w", encoding='utf-8') as file:
            file.write(html_response)

        with open(f"data/index_{i}.html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all("a", class_="card-details-link")

        for item in cards:
            fest_url = "https://www.skiddle.com" + item.get("href")
            fests_urls_list.append(fest_url)
    print(fests_urls_list)




chek_directory()
collection_links_festivals()
