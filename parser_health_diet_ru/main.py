import requests
from bs4 import BeautifulSoup
import json
import csv
import os

PARAMS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def save_index_html():
    url = 'https://health-diet.ru/table_calorie/'
    src = requests.get(url, params=PARAMS).text
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src)


def open_index_html():
    with open('index.html', encoding='utf-8') as file:
        src = file.read()
    return src


def text_correction(name: str):
    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in name:
            name = name.replace(item, '_')
    return name


def search_all_catigories(src):
    catigories = dict()
    soup = BeautifulSoup(src, 'lxml')
    all_catigories = soup.find_all(class_='mzr-tc-group-item-href')
    for item in all_catigories:
        name = text_correction(item.text)
        catigories[name] = 'https://health-diet.ru' + item.get('href')
    return catigories


def save_all_catigories_json(all_catigories):
    with open('all_catigories.json', 'w', encoding='utf-8') as file:
        json.dump(all_catigories, file, indent=4, ensure_ascii=False)


def open_all_catigories_json():
    with open('all_catigories.json', encoding='utf-8') as file:
        all_catigories = json.load(file)
    return all_catigories


def chek_directory():
    folder_name = f"data"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
        os.mkdir(folder_name)


def save_catigories_html():
    chek_directory()
    count = len(all_catigories)
    for key, value in all_catigories.items():
        src = requests.get(value, params=PARAMS).text

        with open(f'./data/{key}.html', 'w', encoding='utf-8') as file:
            file.write(src)

        open_catigories(key)
        print(f'Работа с {key}')
        count -= 1


def open_catigories(name: str):
    with open(f'./data/{name}.html', encoding='utf-8') as file:
        src = file.read()
    collection_categories(src, name)


def collection_categories(src: str, name: str):
    soup = BeautifulSoup(src, 'lxml')
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        pass
    else:
        table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text

        with open(f'./data/{name}.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow((product, calories, proteins, fats, carbohydrates))

        products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

        product_info = []
        for item in products_data:
            product_tds = item.find_all("td")

            title = product_tds[0].find("a").text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text

            product_info.append(
                {
                    "Title": title,
                    "Calories": calories,
                    "Proteins": proteins,
                    "Fats": fats,
                    "Carbohydrates": carbohydrates
                }
            )

            with open(f'./data/{name}.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((title, calories, proteins, fats, carbohydrates))

            with open(f"data/{name}.json", "a", encoding="utf-8") as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)


save_index_html()
src = open_index_html()
all_catigories = search_all_catigories(src)
save_all_catigories_json(all_catigories)
all_catigories = open_all_catigories_json()
save_catigories_html()
