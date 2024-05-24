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

#sudo apt-get install chromium-chromedriver
#python -m pip install pyvirtualdisplay
#sudo apt-get install xvfb

ispi = True

if(ispi):
    from pyvirtualdisplay import Display


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

#python -m pip install googletrans
from googletrans import Translator

import os

history = []
f = open("readhistory.txt","r")
for line in f:
    history.append(line.strip())
f.close()

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
        
        #print(content)
    
    #add big header for title
    if(chunks):
        chunks[0] = "# " + chunks[0]
        if(current): #append current if there is anything in it
            chunks.append(current)
    return chunks

def chunkcombiner2(contents):
    chunks = []
    current = ""
    for content in contents:
        #check if url contains "https://" just straight add it
        if "https://" in content:
            #print("entered html")
            if(current):
                chunks.append(current)
            chunks.append(content)
            current = ""
        
        
        if content == "-": #ignore single dashes
            pass
        #elif(len(content) > 2000): #if content itself is bigger than 2000 characters, needs to be broken smaller
        #    #split the words so less than 2000
        #    print("smallchunking")
        #    temphold = content.split() #split into individual words separated by space
        #    tempchunk = ""
        #    
        #    for word in temphold:
        #        if(len(tempchunk) + len(word) + 1 > 2000):
        #            #save this chunk to array and reset
        #            chunks.append(tempchunk)
        #            tempchunk = word
        #            
        #        else:    
        #            tempchunk += word + " " #append word with a spacebar
        
        elif(len(current) + len(content) > 2000): #discord limit 2000 character max append  #if content+current bigger, save the current and start the next
           # print("entered elif ", len(current), len(content))
            #print(current)
            chunks.append(current)
            #reset current
            #current = ""
            current = content
        
        else:
            #print("entered else " + str(len(current))
            current += content + "\n"
            #print("entered else " + str(len(current)))
    
    #add big header for title
    if(chunks):
        chunks[0] = "# " + chunks[0]
        if(current): #append current if there is anything in it
            chunks.append(current)
    
    else: #chunks is empty
        chunks.append(current)
        chunks[0] = "# " + chunks[0]
    
    #print(current)
    return chunks

class Mabiscraper:
    def __init__(self):
        dir_path = os.getcwd()
        if(ispi):
            #for raspberry pi######
            display = Display(visible=0, size=(1600, 1200))
            display.start()
            ########################
            #raspberry pi
            self.options = webdriver.ChromeOptions()
            #self.options.add_argument("--no-sandbox");
            #self.options.add_argument("--disable-dev-shm-usage");
            #self.options.add_argument("--disable-renderer-backgrounding");
            #self.options.add_argument("--disable-background-timer-throttling");
            #self.options.add_argument("--disable-backgrounding-occluded-windows");
            #self.options.add_argument("--disable-client-side-phishing-detection");
            #self.options.add_argument("--disable-crash-reporter");
            #self.options.add_argument("--disable-oopr-debug-crash-dump");
            #self.options.add_argument("--no-crash-upload");
            #self.options.add_argument("--disable-gpu");
            #self.options.add_argument("--disable-extensions");
            #self.options.add_argument("--disable-low-res-tiling");
            #self.options.add_argument("--log-level=3");
            #self.options.add_argument("--silent");
            self.options.add_argument(f'user-data-dir={dir_path}/selenium')
            
            browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
            self.driver = webdriver.Chrome(service=browser_driver, options=self.options)
    
        else:
            #add option to show the chrome window
            options = Options()
            options.add_experimental_option("detach", True)
       
            #keep cookies #only works on windows
            options.add_argument(f'user-data-dir={dir_path}/selenium')
        
            #start the driver
            #windows
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        
        
        self.driver.implicitly_wait(0) #wait infinitely
        
        #get cookies from landing page
        self.driver.get("https://mabinogi.nexon.net/landing")
        
        #can attatch as [pageurl, type]
        #access the pages you want to go to now

    def close(self):
        self.driver.close()
        
#get the the mainpage for specific type of page for NA
#gets the links on the mainpage of given the NALINK and returns the links for articles in that category of NA webpage        
    def start(self,link):
        self.driver.get(link)

        #find the divs containing the actual page to the page article
        #target "a" with "c-loadmore-items" class
        anchors = self.driver.find_elements("xpath", "//div[contains(@class, 'c-loadmore-items__initial-products')]/a")

        #get the links on the specified main "news" page by looking at the href
        links = []
        for anchor in anchors:
            link = anchor.get_attribute("href")
            if not(link in history): #if link hasnt been read before
                links.append(link)
                f = open("readhistory.txt","a+")
                f.write(link+"\n")
                f.close()
                history.append(link)
                print("added " + link)
        print(links)
        return links

    def startKR(self,link):
        self.driver.get(link)
        
        #target (ul class="notice">li>dl>dt>a   /li/dl/dt/a
        anchors = self.driver.find_elements("xpath","//ul[@class='notice']/li/dl/dt/a")
        links = []
        #print(anchors)
        for anchor in anchors:
            link = anchor.get_attribute("href")
            if not(link in history): #if link hasnt been read before
                links.append(link)
                f = open("readhistory.txt","a+")
                f.write(link+"\n")
                f.close()
                history.append(link)
                print("added " + link)
        print(links)
        return links

    def getarticledata(self,link):
        #check the pages and print the info
        self.driver.get(link)    

        pagecontents = []
        #article title
        title = self.driver.find_elements(By.CLASS_NAME, "news-detail-header__title-text")
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
        article = self.driver.find_elements("xpath", "//div[contains(@class, 'news-detail-article-body')]/div/*")
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
                        #print("textis2 " +source["src"])
                        pagecontents.append(source["src"])
                    
            splitlines = text.splitlines()
            for line in splitlines:
                if(line): #if not empty string
                    #print("textis " + repr(line))
                    pagecontents.append(line)
        
        return pagecontents

    def getarticledataKR(self,link):
        #title in //div[@class='board_view01']/dl/dt/
        #content in //dd[@view_cont_wrap/div[@view_cont]/*
        self.driver.get(link)
        
        translator = Translator()
        
        pagecontents=[]
        
        #get title
        title = self.driver.find_element("xpath", "//div[@class='board_view01']/dl/dt")
        title = title.get_attribute("innerHTML")
        #soup = BeautifulSoup(tit)
        soup = BeautifulSoup(title, features="lxml")
        text = soup.get_text()
        
        splitlines = text.splitlines()
        for line in splitlines:
            if(line): #if not empty string
                #print("textis " + line)
                tlline = translator.translate(line, dest="en", src="ko")
                pagecontents.append(tlline.text)
        
        #get article content
        article = self.driver.find_elements("xpath", "//dd[@class='view_cont_wrap']/div[@class='view_cont']/*")
        #print(article)
        for content in article:
            #print(content.get_attribute("innerHTML"))
            #print()
            arti = content.get_attribute("innerHTML")
            
            arti = arti.replace("<br>", "\n")
            soup = BeautifulSoup(arti, features="lxml")
            text = soup.get_text()
            
            text = text.replace('\xa0','')
            
            if(text == ""):
                for source in soup.select("[src]"):
                    
                    if(source["src"]):
                        #print(source["src"])
                        #print("textis2 " +source["src"])
                        pagecontents.append(source["src"])
                    
            splitlines = text.splitlines()
            for line in splitlines:
                if(line): #if not empty string
                    print("textis " + repr(line))
                    try:
                        tlline = translator.translate(line, dest="en", src="ko")
                    except:
                        pass
                    if tlline is None:
                        pass
                    else:
                        pagecontents.append(tlline.text)
        
        #print(pagecontents)
        return pagecontents


NALINKS = [
    "https://mabinogi.nexon.net/news/announcements",
    "https://mabinogi.nexon.net/news/updates",
    "https://mabinogi.nexon.net/news/events",
    "https://mabinogi.nexon.net/news/sales",
    "https://mabinogi.nexon.net/news/community",
    "https://mabinogi.nexon.net/news/maintenance"
]

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

KRLINKS = [
"https://mabinogi.nexon.com/page/news/notice_list.asp?searchtype=91&searchword=%B0%F8%C1%F6"
]

