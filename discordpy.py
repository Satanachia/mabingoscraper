import os

import discord
from dotenv import load_dotenv

import time

from threading import Thread
from threading import Lock

from discord.ext import tasks

import datetime
#python -m pip install datetime

import Mabiscraper

#python -m pip install discord.py
#python -m pip install googletrans==3.1.0a0

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents(messages=True, guilds=True, message_content=True)
client = discord.Client(intents=intents)

NALINKS = [
        "https://mabinogi.nexon.net/news/announcements",
        "https://mabinogi.nexon.net/news/updates",
        "https://mabinogi.nexon.net/news/events",
        "https://mabinogi.nexon.net/news/sales",
        "https://mabinogi.nexon.net/news/community",
        "https://mabinogi.nexon.net/news/maintenance"]

KRLINKS = [
"https://mabinogi.nexon.com/page/news/notice_list.asp?searchtype=91&searchword=%B0%F8%C1%F6"
]

scraperlock = Lock()

async def test(channel, links, scraper):
    for link in links:
        pagecontents = scraper.getarticledata(link)
        chunked = Mabiscraper.chunkcombiner(pagecontents)
        print(chunked)
        await channel.send("# =-----------------------------------------------------------=")
        for pagecontent in chunked:
            await channel.send(pagecontent)
        await channel.send(link)

async def transtest(channel, links, scraper):
    for link in links:
        pagecontents = scraper.getarticledataKR(link)
        chunked = Mabiscraper.chunkcombiner2(pagecontents)
        #print(chunked)
        #for chunk in chunked:
        #    print(len(chunk))
        #    print(chunk)
        await channel.send("# =-----------------------------------------------------------=")
        for pagecontent in chunked:
            await channel.send(pagecontent)
        await channel.send(link)

async def runcheckpages():
    try:
        scraperlock.acquire()
        await checkpages()
    except Exception as e:
        print("error running checkpages()")
        print(e)
    finally:
        scraperlock.release()

#starts the scraper, checks the pages, posts the information and closes the scraper
async def checkpages():
    guild = variables['guild']
    CHannounceEN = discord.utils.get(guild.channels, name="eng-announce")
    CHupdatesEN = discord.utils.get(guild.channels, name="eng-updates")
    CHeventsEN = discord.utils.get(guild.channels, name="eng-events")
    CHsalesEN = discord.utils.get(guild.channels, name="eng-sales")
    CHcommunityEN = discord.utils.get(guild.channels, name="eng-community")
    CHmaintenanceEN = discord.utils.get(guild.channels, name="eng-maintenance")
    
    CHnotificationKR = discord.utils.get(guild.channels, name="kr-notification")
    
    print(CHannounceEN)
    #print(CHannounceEN.id)
    #for i in range(20):
    #    await CHannounceEN.send(f"test{i}")
    
    #can only use 1 scraper at a time
    scraper1 = Mabiscraper.Mabiscraper()
    
    #loop this section
    #NA Side
    links1 = scraper1.start(NALINKS[0])
    links2 = scraper1.start(NALINKS[1])
    links3 = scraper1.start(NALINKS[2])
    links4 = scraper1.start(NALINKS[3])
    links5 = scraper1.start(NALINKS[4])
    links6 = scraper1.start(NALINKS[5])
    
    await test(CHannounceEN, links1, scraper1)
    await test(CHupdatesEN, links2, scraper1)
    await test(CHeventsEN, links3, scraper1)
    await test(CHsalesEN, links4, scraper1)
    await test(CHcommunityEN, links5, scraper1)
    await test(CHmaintenanceEN, links6, scraper1)
    
    #KR Side
    klinks1 = scraper1.startKR(KRLINKS[0])
    await transtest(CHnotificationKR, klinks1, scraper1)
    
    print("cycle done")
    #need to add code to repeat and make sure its not running the same link again
    
    scraper1.close()
    
variables = {}
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    variables['guild'] = guild
    #variables['client'] = client
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    #get the channels to send to
    
    
    #CHannounceEN = discord.utils.get(guild.channels, name="eng-announce")
    #CHupdatesEN = discord.utils.get(guild.channels, name="eng-updates")
    #CHeventsEN = discord.utils.get(guild.channels, name="eng-events")
    #CHsalesEN = discord.utils.get(guild.channels, name="eng-sales")
    #CHcommunityEN = discord.utils.get(guild.channels, name="eng-community")
    #CHmaintenanceEN = discord.utils.get(guild.channels, name="eng-maintenance")
    #
    #CHnotificationKR = discord.utils.get(guild.channels, name="kr-notification")
    #
    #print(CHannounceEN)
    ##print(CHannounceEN.id)
    ##for i in range(20):
    ##    await CHannounceEN.send(f"test{i}")
    #
    ##can only use 1 scraper at a time
    #scraper1 = Mabiscraper.Mabiscraper()
    #
    ##loop this section
    ##NA Side
    #links1 = scraper1.start(NALINKS[0])
    #links2 = scraper1.start(NALINKS[1])
    #links3 = scraper1.start(NALINKS[2])
    #links4 = scraper1.start(NALINKS[3])
    #links5 = scraper1.start(NALINKS[4])
    #links6 = scraper1.start(NALINKS[5])
    #
    #await test(CHannounceEN, links1, scraper1)
    #await test(CHupdatesEN, links2, scraper1)
    #await test(CHeventsEN, links3, scraper1)
    #await test(CHsalesEN, links4, scraper1)
    #await test(CHcommunityEN, links5, scraper1)
    #await test(CHmaintenanceEN, links6, scraper1)
    #
    ##KR Side
    #klinks1 = scraper1.startKR(KRLINKS[0])
    #await transtest(CHnotificationKR, klinks1, scraper1)
    #
    #print("cycle done")
    ##need to add code to repeat and make sure its not running the same link again
    #
    #scraper1.close()
    
    ##await checkpages()
    
    autoloop.start()
    
   ## await client.close()
   
    #print(links)
    #for link in links:
    #    await test(CHannounceEN, links, scraper.driver)

@client.event
async def on_message(message):
    #print("---------")
    #print(message)
    #print(message.content)
    #print(message.channel)
    
    msgtxt = message.content
    msgchannel = message.channel.name
    publicchannel = False
    privatechannel = False

    if(msgchannel == "botmanual"):
        publicchannel = True
    if(msgchannel == "shutdown"):
        privatechannel = True

    if(publicchannel and msgtxt == "check"):
        await message.channel.send("Starting Check")
        await runcheckpages()
            
        await message.channel.send("Check Completed")
        
    elif(privatechannel and msgtxt == "shutdown"):
        await message.channel.send("Shutting Down")
        await client.close()

utc = datetime.timezone.utc
#loop every 4 hours
#5:05pm pst
#1:05pm kst
times = [
    datetime.time(hour=0, minute=5, tzinfo=utc), #5:05pm pst
    datetime.time(hour=4, minute=5, tzinfo=utc) #1:05pm kst
]


#@tasks.loop(hours=2)
@tasks.loop(time=times)
async def autoloop():
    guild = variables["guild"]
    channel = discord.utils.get(guild.channels, name="botauto")
    await channel.send("Starting Auto")
    await runcheckpages()
    
    await channel.send("Completed")


def job():
#loop this section specified time
    client.run(TOKEN)
#schedule.every().day.at("18:30").do(job,"NA")
#schedule.every().day.at("05:00").do(job,"other half")
#
#while True:
#    schedule.run_pending()
#    time.sleep(60)

job()
