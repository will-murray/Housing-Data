from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re


# path = 'https://victoria.craigslist.org/search/victoria-bc/hhh?lat=48.4654&lon=-123.3276&search_distance=2#search=1~gallery~0~0'
path = 'https://vancouver.craigslist.org/search/vancouver-bc/hhh?lat=49.2875&lon=-123.1308&postedToday=1&search_distance=0.8#search=1~gallery~0~0'

def extract_int_from_xbr(s):
    match = re.search(r'(\d+)br', s)
    if match:
        x_str = match.group(1)
        x = int(x_str)
        return x
    else:
        return "NA"
    
def scrape_text_data(driver):
    cards = driver.find_elements(By.CLASS_NAME, "cl-search-result")
    print("scraped cards sucessfully... ")
    print(f"observations before processing: ", len(cards))
    data = []

    for card in cards:
        try:
            price = card.find_element(By.CLASS_NAME, "priceinfo").text
            meta = card.find_element(By.CLASS_NAME, "meta").text
            title = card.find_element(By.CLASS_NAME, "titlestring").text
        except NoSuchElementException:
            price = "NA"
            meta = "NA"
            title = "NA"

        data.append([price, meta, title])
    return data


def format_text_data(data):
    for listing in data:
        if listing[0] == "NA":
            data.remove(listing)
        else:

            listing[0] = int(re.sub(r'\$|,', '', listing[0]))
            listing[1] = extract_int_from_xbr(listing[1])
            if listing[1] == "NA":
                data.remove(listing)

    result = []
    for listing in data:
        if (type(listing[0]) == int and type(listing[1] == int) and listing[0] <= 10000):
            result.append(listing)

    return result


def get_gallery_cards():
    driver = webdriver.Edge()

    driver.get(path)
    driver.implicitly_wait(10)

    data = scrape_text_data(driver)
    result = format_text_data(data)

    print("observations after processing :", len(result))
    return result


cards = get_gallery_cards()
for card in cards:
    print(card)
