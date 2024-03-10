import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
client = discord.Client()

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
    print(CHannounceEN)
    print(CHannounceEN.id)
    for i in range(20):
        await CHannounceEN.send(f"test{i}")
    
    
    
client.run(TOKEN)

#print(TOKEN)
