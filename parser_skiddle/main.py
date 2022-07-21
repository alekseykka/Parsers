import requests
from bs4 import BeautifulSoup
import json
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def chek_directory_data():
    folder_name = f"data"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
        os.mkdir(folder_name)


def save_page_index_html():
    for i in range(0, 168, 24):
        url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=" \
              f"20%20Jul%202022&to_date=&maxprice=500&o={i}&bannertitle=July"

        req = requests.get(url=url, headers=HEADERS)
        json_data = json.loads(req.text)
        html_response = json_data["html"]

        with open(f"data/index_{i}.html", "w", encoding='utf-8') as file:
            file.write(html_response)


def open_page_index_html(i: int):
    with open(f"data/index_{i}.html", encoding='utf-8') as file:
        src = file.read()
    return src


def collection_all_liks():
    fests_urls_list = []
    for i in range(0, 168, 24):
        src = open_page_index_html(i)
        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all("a", class_="card-details-link")

        for item in cards:
            link_festival = item.get("href")
            fest_url = "https://www.skiddle.com" + link_festival
            fests_urls_list.append(fest_url)
    collection_page(fests_urls_list)


def save_json_festivals(fest_list_result: list):
    with open("festivals.json", "w", encoding="utf-8") as file:
        json.dump(fest_list_result, file, indent=4, ensure_ascii=False)


def getting_html_code(link: str):
    req = requests.get(url=link, headers=HEADERS).text
    soup = BeautifulSoup(req, 'lxml')
    return soup


def collection_page(links: list):
    fest_list_result = []
    for link in links:
        try:
            print(link)
            fest_code = getting_html_code(link)

            name_fest = fest_code.find('h1').text.strip()
            date_fest = fest_code.find('h3').text.strip()
            fest_location_url = "https://www.skiddle.com" + fest_code.find("a", class_="tc-white").get("href").strip()
            restrictions_fest = fest_code.find('h3').find_next('p').find_next('p').text.strip()
            logo_url = fest_code.find('source').get('srcset')

            location_code = getting_html_code(fest_location_url)
            location_info = location_code.find('h2', string="Venue contact details and info").find_next()
            items = [item.text for item in location_info.find_all('p')]

            contacts_detail = {}
            for item in items:
                item = item.split(':')
                if len(item) == 3:
                    contacts_detail[item[0].strip()] = f"{item[1].strip()}:{item[2].strip()}"
                else:
                    contacts_detail[item[0].strip()] = item[1].strip()

            fest_list_result.append(
                {
                    "Fest name": name_fest,
                    "Fest date": date_fest,
                    "Fest restrictions (age)": restrictions_fest,
                    "Fest logo": logo_url,
                    "Contacts data": contacts_detail
                }
            )
        except AttributeError:
            print(AttributeError)

    save_json_festivals(fest_list_result)


if __name__ == '__main__':
    chek_directory_data()
    save_page_index_html()
    collection_all_liks()
