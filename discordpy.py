import os

import discord
from dotenv import load_dotenv

import Mabiscraper

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
client = discord.Client()

NALINKS = [
        "https://mabinogi.nexon.net/news/announcements",
        "https://mabinogi.nexon.net/news/updates",
        "https://mabinogi.nexon.net/news/events",
        "https://mabinogi.nexon.net/news/sales",
        "https://mabinogi.nexon.net/news/community",
        "https://mabinogi.nexon.net/news/maintenance"]

async def test(channel, links, driver):
    for link in links:
        pagecontents = Mabiscraper.getarticledata(driver, link)
        chunked = Mabiscraper.chunkcombiner(pagecontents)
        print(chunked)
        await channel.send("# =-----------------------------------------------------------=")
        for pagecontent in chunked:
            await channel.send(pagecontent)
        await channel.send(link)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    #get the channels to send to
    
    
    CHannounceEN = discord.utils.get(guild.channels, name="eng-announce")
    CHupdatesEN = discord.utils.get(guild.channels, name="eng-updates")
    CHeventsEN = discord.utils.get(guild.channels, name="eng-events")
    CHsalesEN = discord.utils.get(guild.channels, name="eng-sales")
    CHcommunityEN = discord.utils.get(guild.channels, name="eng-community")
    CHmaintenanceEN = discord.utils.get(guild.channels, name="eng-maintenance")
    
    print(CHannounceEN)
    #print(CHannounceEN.id)
    #for i in range(20):
    #    await CHannounceEN.send(f"test{i}")
    
    #can only use 1 scraper at a time
    scraper1 = Mabiscraper.Mabiscraper()
    links1 = Mabiscraper.start(scraper1.driver, NALINKS[0])
    links2 = Mabiscraper.start(scraper1.driver, NALINKS[1])
    links3 = Mabiscraper.start(scraper1.driver, NALINKS[2])
    links4 = Mabiscraper.start(scraper1.driver, NALINKS[3])
    links5 = Mabiscraper.start(scraper1.driver, NALINKS[4])
    links6 = Mabiscraper.start(scraper1.driver, NALINKS[5])
    
    await test(CHannounceEN, links1, scraper1.driver)
    await test(CHupdatesEN, links2, scraper1.driver)
    await test(CHeventsEN, links3, scraper1.driver)
    await test(CHsalesEN, links4, scraper1.driver)
    await test(CHcommunityEN, links5, scraper1.driver)
    await test(CHmaintenanceEN, links6, scraper1.driver)
    
    
    #print(links)
    #for link in links:
    #    await test(CHannounceEN, links, scraper.driver)
        
    
client.run(TOKEN)

#print(TOKEN)
