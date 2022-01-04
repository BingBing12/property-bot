from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time

chrome_driver_path = "C:\development\chromedriver.exe"
ser = Service(chrome_driver_path)

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfbFxqS05JV2a-ZOw_bUHy-ySMpH5u5LRhNQtP4GOXLuJgjow/viewform?usp=sf_link"

zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.618817799424754%2C%22north%22%3A37.931434633982654%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22price%22%3A%7B%22max%22%3A588823%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}

response = requests.get(zillow_url, headers=headers)
web_html = response.text

soup = BeautifulSoup(web_html, "html.parser")
listings = soup.select(selector="#grid-search-results .list-card-info a")
prices = soup.select(selector="#grid-search-results .list-card-price")

listing_data = {}

for (index, listing) in enumerate(listings):
    link = listing.get("href")
    if "https://www.zillow.com" not in link:
        link = f"https://www.zillow.com{link}"

    listing_data[index] = {
        0: listing.text,
        1: link,
        2: prices[index].text,
    }
driver = webdriver.Chrome(service=ser)
driver.get(FORM_URL)
time.sleep(1)
for data in listing_data.values():
    print(data)
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="input.quantumWizTextinputPaperinputInput")
    submit = driver.find_element(by=By.CSS_SELECTOR, value=".appsMaterialWizButtonPaperbuttonLabel")

    for (index, answer) in enumerate(inputs):
        print(data[index])
        answer.send_keys(data[index])

    submit.click()
    another_response = driver.find_element(by=By.CSS_SELECTOR, value=".freebirdFormviewerViewResponseLinksContainer a")
    another_response.click()




