import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# get data from the page you want to scrap, make sure you are using Chrome of Safari
header = {
    "User-Agent": "Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
WEBSITE = "https://www.zillow.com/toronto-on/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Toronto%2C%20ON%22%2C%22mapBounds%22%3A%7B%22west%22%3A-79.43920078464575%2C%22east%22%3A-79.33877887912817%2C%22south%22%3A43.62683946453325%2C%22north%22%3A43.67813564568663%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A792680%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D"
response = requests.get(WEBSITE,headers=header)
data=response.text
soup = BeautifulSoup(data, 'lxml')

# scrap links for each rental
all_link_elements = soup.select(".list-card-info a")
all_links = []
for link in all_link_elements:
    href=link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

# scrap addresses for each rental
all_address_elements = soup.select(".list-card-addr")
all_addresses = [address.get_text() for address in all_address_elements]

# scrap prices for each rental
all_price_elements = soup.select(".list-card-price")
all_prices=[price.get_text().split("+")[0].split("/")[0] for price in all_price_elements]

# fill scrapped data into google form
chrome_driver_path = ".../chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
# create a google form including address, price, and link sections for auto-fill
GOOGEL_FORM = ""
for n in range(len(all_links)):
    driver.get(GOOGEL_FORM)
    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    # submit data for each rental
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()