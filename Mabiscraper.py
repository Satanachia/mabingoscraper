#https://mabinogi.nexon.net/news/announcements
#https://mabinogi.nexon.net/news/updates
#https://mabinogi.nexon.net/news/events
#https://mabinogi.nexon.net/news/sales
#https://mabinogi.nexon.net/news/community
#https://mabinogi.nexon.net/news/maintenance

#https://realpython.com/python-web-scraping-practical-introduction/

#python -m pip install selenium
#python -m pip install webdriver_manager
#python -m pip install bs4
#python -m pip install lxml

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import os

#for NA
def getarticledata(driver,link):
    #check the pages and print the info
    driver.get(link)    

    pagecontents = []
    #article title
    title = driver.find_elements(By.CLASS_NAME, "news-detail-header__title-text")
    for titl in title:
        #print(titl.get_attribute("innerHTML"))
        #print()
        tit = titl.get_attribute("innerHTML")
        #soup = BeautifulSoup(tit)
        soup = BeautifulSoup(tit, features="lxml")
        text = soup.get_text()
        
        splitlines = text.splitlines()
        for line in splitlines:
            if(line): #if not empty string
                #print("textis " + line)
                pagecontents.append(line)
        
    #article info
    #look for div with class "news-detail-article-body and target anything in the child's div"
    article = driver.find_elements("xpath", "//div[contains(@class, 'news-detail-article-body')]/div/*")
    for content in article:
        #print(content.get_attribute("innerHTML"))
        #print()
        arti = content.get_attribute("innerHTML")
        soup = BeautifulSoup(arti, features="lxml")
        text = soup.get_text()
        
        text = text.replace('\xa0','')
        
        if(text == ""):
            for source in soup.select("[src]"):
                
                if(source["src"]):
                    #print(source["src"])
                    print("textis2 " +source["src"])
                    pagecontents.append(source["src"])
                
        splitlines = text.splitlines()
        for line in splitlines:
            if(line): #if not empty string
                print("textis " + repr(line))
                pagecontents.append(line)
    
    return pagecontents

#combines each line read into chunks up to the 2000 character discord limit to alleviate rate limiting on discord
#send more lines at once is better than sending one line at a time
def chunkcombiner(contents):
    chunks = []
    current = ""
    for content in contents:
        #check if url contains "https://"
        if "https://" in content:
            if(current):
                chunks.append(current)
            chunks.append(content)
            current = ""
        
        elif(len(current) + len(content) > 2000): #discord limit 2000 character max
            chunks.append(current)
            #reset current
            current = ""
        
        else:
            current += content + "\n"
    
    #add big header for title
    if(chunks):
        chunks[0] = "# " + chunks[0]
        if(current): #append current if there is anything in it
            chunks.append(current)
    return chunks

class Mabiscraper:
    def __init__(self):
        #add option to show the chrome window
        options = Options()
        options.add_experimental_option("detach", True)
        
        #keep cookies
        dir_path = os.getcwd()
        options.add_argument(f'user-data-dir={dir_path}/selenium')
        
        #start the driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        #get cookies from landing page
        self.driver.get("https://mabinogi.nexon.net/landing")
        
        #can attatch as [pageurl, type]
        #access the pages you want to go to now



NALINKS = [
        "https://mabinogi.nexon.net/news/announcements",
        "https://mabinogi.nexon.net/news/updates",
        "https://mabinogi.nexon.net/news/events",
        "https://mabinogi.nexon.net/news/sales",
        "https://mabinogi.nexon.net/news/community",
        "https://mabinogi.nexon.net/news/maintenance"]

##add option to show the chrome window
#options = Options()
#options.add_experimental_option("detach", True)
#
##keep cookies
#dir_path = os.getcwd()
#options.add_argument(f'user-data-dir={dir_path}/selenium')
#
##start the driver
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
##get cookies from landing page
#driver.get("https://mabinogi.nexon.net/landing")
#
##can attatch as [pageurl, type]
##access the pages you want to go to now
#NALINKS = [
#"https://mabinogi.nexon.net/news/announcements",
#"https://mabinogi.nexon.net/news/updates",
#"https://mabinogi.nexon.net/news/events",
#"https://mabinogi.nexon.net/news/sales",
#"https://mabinogi.nexon.net/news/community",
#"https://mabinogi.nexon.net/news/maintenance"]

#get the the mainpage for specific type of page
def start(driver,link):
    driver.get(link)
    driver.implicitly_wait(2)

    #find the divs containing the actual page to the page article
    #target "a" with "c-loadmore-items" class
    anchors = driver.find_elements("xpath", "//div[contains(@class, 'c-loadmore-items__initial-products')]/a")

    #get the links on the specified main "news" page by looking at the href
    links = []
    for anchor in anchors:
        link = anchor.get_attribute("href")
        links.append(link)
        print(link)
    return links

#scraper = Mabiscraper()
#links = start(scraper.driver, NALINKS[1])
#data = getarticledata(scraper.driver, links[0])
#chunked = chunkcombiner(data)
#print("______________________________")
#print(chunked)


