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


def text_correction(name: str):
    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in name:
            name = name.replace(item, '_')
    return name


def chek_directory():
    folder_name = f"data"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
        os.mkdir(folder_name)


def save_file(name: str, form: str, data: str | tuple | list):
    with open(f'{name}.{form}', 'a', encoding='utf-8', newline='') as file:
        if form == "html":
            file.write(data)
        elif form == "csv":
            writer = csv.writer(file)
            writer.writerow(data)
        elif form == "json":
            json.dump(data, file, indent=4, ensure_ascii=False)


def open_file(name: str, form: str):
    with open(f'{name}.{form}', encoding='utf-8') as file:
        if form == "html":
            return file.read()
        elif form == "json":
            return json.load(file)


def search_all_catigories(src: str):
    catigories = dict()
    soup = BeautifulSoup(src, 'lxml')
    all_catigories = soup.find_all(class_='mzr-tc-group-item-href')
    for item in all_catigories:
        name = text_correction(item.text)
        catigories[name] = 'https://health-diet.ru' + item.get('href')
    return catigories


def get_page():
    url = 'https://health-diet.ru/table_calorie/'
    src = requests.get(url, params=PARAMS).text

    save_file("index", "html", src)

    url_catigories = search_all_catigories(src)

    for key, value in url_catigories.items():
        src = requests.get(value, params=PARAMS).text

        save_file(f'./data/{key}', "html", src)

        src = open_file(f'./data/{key}', "html")
        print(value)
        get_info(src, key)


def get_info(src: str, name: str):
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

        save_file(f"./data/{name}", "csv", (product, calories, proteins, fats, carbohydrates))

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

            save_file(f"./data/{name}", "csv", (title, calories, proteins, fats, carbohydrates))

            save_file(f"./data/{name}", "json", product_info)


def main():
    chek_directory()
    get_page()


if __name__ == '__main__':
    main()
