import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
#CHANNEL_ID = 1252078526564401182

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('ready on')
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('進捗どうですか')

client.run(TOKEN)
