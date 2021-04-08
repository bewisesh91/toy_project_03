from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


client = MongoClient('localhost', 27017)
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.db_flask_practice3

driver = webdriver.Chrome('./chromedriver')

url = "http://matstar.sbs.co.kr/location.html"

driver.get(url)
time.sleep(5)

# 버튼 선택하기
# btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
# btn_more.click()
# time.sleep(5)

# 버튼 10번 선택하
for i in range(10):
    try:
        btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    except NoSuchElementException:
        break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("ul.restaurant_list > div > div > li > div > a")
print(len(places))

for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
    # print(title, address, category, show, episode)

    # geocode를 이용해서 x, y좌표 확인하기
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "es14wzgnxt",
        "X-NCP-APIGW-API-KEY": "qtNELykjPXgox55bfAeJ8tNdsi9LwOhbtfpFpkw0"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()
    # response를 확인해보면 adresses안에 x, y가 있는 것을 확인할 수 있다.
    # print(response)

    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            doc = {
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)
        else:
            print(title, "좌표를 찾지 못했습니다")

