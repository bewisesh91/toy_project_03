from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


driver = webdriver.Chrome('./chromedriver')

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%AA%A8%EB%B9%8C%EB%A6%AC%ED%8B%B0&oquery=%EB%AA%A8%EB%B9%8C%EB%A6%AC%ED%8B%B0&tqi=hbIphsprvmsssPcJLAGssssssdZ-264575"
driver.get(url)
sleep(3)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
news_list = soup.select(".bx .news_tit")
print(len(news_list))

for news in news_list:
    src = news["href"]
    print(src)

