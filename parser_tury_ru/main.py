from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import csv


def create_webdriver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def chek_directory_data():
    folder_name = f"data"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
        os.mkdir(folder_name)


def save_html_file(req: str, i: int):
    with open(f"data/index_{i}.html", "w", encoding="utf-8") as file:
        file.write(req)


def collection_html():
    driver = create_webdriver()
    try:
        for i in range(0, 90, 30):
            url = f"https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most&hotel_link=/hotel/id/%HOTEL_ID%&r=107128913&s={i}"
            driver.get(url=url)
            time.sleep(10)
            save_html_file(driver.page_source, i)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def open_html_file(i: int):
    with open(f"data/index_{i}.html", encoding="utf-8") as file:
        src = file.read()
    return src


def save_links_CSV(name="name", url="url"):
    with open(f'links.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow((name, url))


def collectoin_links_hotels():
    save_links_CSV()
    for i in range(0, 90, 30):
        src = open_html_file(i)
        soup = BeautifulSoup(src, "lxml").find_all("a", class_="hotel_name")
        for info in soup:
            name_hotel = info.find_next("b").text
            url_hotel = "https://www.tury.ru" + info.get("href")
            save_links_CSV(name_hotel, url_hotel)


def main():
    chek_directory_data()
    collection_html()
    collectoin_links_hotels()


if __name__ == '__main__':
    main()
