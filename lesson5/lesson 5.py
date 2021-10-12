from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as se
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

chrome_options = Options()
chrome_options.add_argument("start-maximized")



driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')

wait = ui.WebDriverWait(driver, 30)
button = driver.find_element(By.CLASS_NAME,'modal-layout__close')
button.click()

for i in range(2):
    articles = driver.find_elements(By.TAG_NAME, 'mvid-promotions-carousel')
    actions = ActionChains(driver)
    actions.key_down(Keys.PAGE_DOWN)
    actions.perform()
    time.sleep(4)


wait = ui.WebDriverWait(driver, 10)
tab_button = driver.find_element(By.XPATH,".//button[@class='tab-button ng-star-inserted']")
tab_button.click()

while True:
    try:
        button = driver.find_elements(By.XPATH, '//mvid-shelf-group/*//button[contains(@class,"btn forward")]/mvid-icon[@type="chevron_right"]')
        button[1].click()
        time.sleep(4)
    except se.ElementNotInteractableException:
        break

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
collection = db.all_goods

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}

response = requests.get("https://www.mvideo.ru/")
dom = html.fromstring(response.text)

items = dom.xpath("//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")


all_goods =[]
for item in items:
    goods = {}
    name = item.find_eiement(By.TAG_NAME, "a").text
    link = item.find_eiement(By.TAG_NAME, "a").get_atrribute("href")
    goods['name'] = name
    goods['link'] = link
    all_goods.append(goods)

    try:
        db.all_goods.incert_one(goods)
        db.all_goods.create_index('link',unique = True)
    except dke:
        continue

pprint(all_goods)
