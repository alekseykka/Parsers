from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import csv


def chek_directory_data():
    folder_name = f"data"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
        os.mkdir(folder_name)


def save_file(name: str, data: str | tuple, form: str):
    with open(f'{name}.{form}', 'a', encoding='utf-8', newline='') as file:
        if form == "html":
            file.write(data)
        elif form == "csv":
            writer = csv.writer(file)
            writer.writerow(data)


def open_html_file(i: int):
    with open(f"data/index_{i}.html", encoding="utf-8") as file:
        src = file.read()
    return src


def get_html():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        for i in range(0, 90, 30):
            url = f"https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most&hotel_link=/hotel/id/%HOTEL_ID%&r=107128913&s={i}"
            driver.get(url=url)
            time.sleep(5)
            save_file(f"data/index_{i}", driver.page_source, "html")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_links_hotels():
    save_file("hotels", ("name", "Url"), "csv")
    for i in range(0, 90, 30):
        src = open_html_file(i)
        soup = BeautifulSoup(src, "lxml").find_all("a", class_="hotel_name")
        for info in soup:
            name_hotel = info.find_next("b").text
            url_hotel = "https://www.tury.ru" + info.get("href")
            save_file("hotels", (name_hotel, url_hotel), "csv")


def main():
    chek_directory_data()
    get_html()
    get_links_hotels()


if __name__ == '__main__':
    main()
