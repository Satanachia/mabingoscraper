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

from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


#for NA
def getarticledata(insertdriver, link):
    #check the pages and print the info
    insertdriver.get(link)    

    #article title
    title = insertdriver.find_elements(By.CLASS_NAME, "news-detail-header__title-text")
    for titl in title:
        #print(titl.get_attribute("innerHTML"))
        #print()
        tit = titl.get_attribute("innerHTML")
        soup = BeautifulSoup(tit, features="lxml")
        text = soup.get_text()
        print(text)
        
    #article info
    #look for div with class "news-detail-article-body and target anything in the child's div"
    article = insertdriver.find_elements("xpath", "//div[contains(@class, 'news-detail-article-body')]/div/*")
    for content in article:
        #print(content.get_attribute("innerHTML"))
        #print()
        arti = content.get_attribute("innerHTML")
        soup = BeautifulSoup(arti, features="lxml")
        text = soup.get_text()
        print(text)

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#get cookies from landing page
driver.get("https://mabinogi.nexon.net/landing")

#print(driver.get_cookies())

#access the pages you want to go to now
driver.get("https://mabinogi.nexon.net/news/announcements")
driver.implicitly_wait(2)
#target "a" with "c-loadmore-items" class
news_a = driver.find_elements("xpath", "//div[contains(@class, 'c-loadmore-items__initial-products')]/a")

#get the news link by looking at the href
news_links = []
for news_link in news_a:
    link = news_link.get_attribute("href")
    news_links.append(link)
    print(link)

#spacing
print()
print()

#test
#getarticledata(driver, news_links[0])
getarticledata(driver, news_links[1])
#getarticledata(driver, news_links[2])
##########

##check the pages and print the info
#driver.get(news_links[0])    
#
##article title
#title = driver.find_elements(By.CLASS_NAME, "news-detail-header__title-text")
#for titl in title:
#    print(titl.get_attribute("innerHTML"))
#    print()
#
##article info
##look for div with class "news-detail-article-body and target anything in the child's div"
#article = driver.find_elements("xpath", "//div[contains(@class, 'news-detail-article-body')]/div/*")
#for content in article:
#    print(content.get_attribute("innerHTML"))
#    print()

#print(article.get_attribute("outerHTML"))
