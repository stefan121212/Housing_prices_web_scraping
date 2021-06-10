from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

# check this link for results -- https://docs.google.com/spreadsheets/d/1AdsK73BiPKEK8jA2FSP3HM8UOKhl-DNHTPS3Mh6gCcI/edit#gid=1898995618

SAN_FRANCISCO = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%2" \
                "2mapBounds%22%3A%7B%22west%22%3A-122.95826985530766%2C%22east%22%3A-122.15489461116704%2C%22south%" \
                "22%3A37.582300194197025%2C%22north%22%3A38.03473744179256%7D%2C%22mapZoom%22%3A11%2C%22isMapVisibl" \
                "e%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A898630%7D%2C%22" \
                "beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%2" \
                "2%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22ah%22%3A%7B%22value%22%3Atrue" \
                "%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7" \
                "B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afals" \
                "e%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isList" \
                "Visible%22%3Atrue%7D"

parameters = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/89.0.4389.114 Safari/537.36",
    "Accept-Language":"sr-RS,sr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,fr;q=0.5,hr;q=0.4,tr;q=0.3,bs;q=0.2"
}

QUESTIONARE = "https://docs.google.com/forms/d/e/1FAIpQLSeyI1tq5obx0P4VDxJtbKJYHEQEEvqEfutzWVRJQ6ISyWhueA" \
              "/viewform?usp=sf_link"
CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"

# formating links because some of them are broken
def format_search_links():
    for n in range(len(links) - 1):
        if "http" not in links[n]:
            links[n] = "https://www.zillow.com" + links[n]


response = requests.get(SAN_FRANCISCO, headers=parameters).text
soup = BeautifulSoup(response, "html.parser")
prices = soup.find_all(class_="list-card-price")
# geting rid of many suficses from prices
prices = [price.text.split("+")[0].split("/")[0].split(" ")[0] for price in prices]
# finding all links because they are broken into 2 different classes
links = soup.find_all("a", class_=["list-card-link list-card-img", "list-card-link list-card-link-top-margin list-card-img"])
links = [link.get("href") for link in links]
format_search_links()
address = soup.find_all(class_="list-card-addr")
address = [adr.text for adr in address]
#uploading info to google form
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(QUESTIONARE)
for n in range(len(prices)):

    sleep(2)
    addr = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    comfirm = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    addr.send_keys(address[n])
    price.send_keys(prices[n])
    link.send_keys(links[n])
    comfirm.click()
    sleep(2)
    next_filling = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_filling.click()
    sleep(2)

driver.close()