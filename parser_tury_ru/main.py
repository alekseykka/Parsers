from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time


def create_webdriver():
    executable_path = "D:\programing\Parsers\parser_tury_ru\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=executable_path)
    return driver


def collection_links(url: str):
    driver = create_webdriver()
    try:
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    url = "https://www.tury.ru/hotel/most_luxe.php"
    collection_links(url)


if __name__ == '__main__':
    main()
