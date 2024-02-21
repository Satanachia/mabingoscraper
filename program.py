#https://mabinogi.nexon.net/news/announcements
#https://mabinogi.nexon.net/news/updates
#https://mabinogi.nexon.net/news/events
#https://mabinogi.nexon.net/news/sales
#https://mabinogi.nexon.net/news/community
#https://mabinogi.nexon.net/news/maintenance

#https://realpython.com/python-web-scraping-practical-introduction/

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detatch", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#get cookies from landing page
driver.get("https://mabinogi.nexon.net/landing")

#print(driver.get_cookies())

#access the pages you want to go to now
driver.get("https://mabinogi.nexon.net/news/announcements")

#target "a" with "c-loadmore-items" class
news_a = driver.find_elements("xpath", "//div[contains(@class, 'c-loadmore-items__initial-products')]/a")

#get the news link by looking at the href
news_links = []
for news_link in news_a:
    link = news_link.get_attribute("href")
    news_links.append(link)
    print(link)

#check the pages and print the info
driver.get(news_links[0])    

#look for div with class "news-detail-article-body"
#article = driver.find_elements("xpath", "//div[contains(@class, 'news-detail-article-body')]")
article = driver.find_elements("xpath", "//div[contains(@class, 'news-detail-article-body')]")
print(article)

test = input("enter")
