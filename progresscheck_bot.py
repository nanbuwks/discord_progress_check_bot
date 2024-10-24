import datetime
import hashlib
import json
import requests
import discord
import os
import sys
from dotenv import load_dotenv
import time
import io
import pandas as pd
# node.json を作成する

googlespreadsheet = "https://docs.google.com/spreadsheets/d/16Viu8d7hSCVY16EFPrGod0wX4e3csOWpnNfiKK85EmA/"
downloadData = requests.get(googlespreadsheet+"export?gid=0&format=csv").content
csvData=downloadData.decode('utf-8')
df = pd.read_csv(io.BytesIO(downloadData),index_col='section',sep=",")
print(df)
#sys.exit()

df.to_json('node.json',orient='index',force_ascii=False) 




# node.json に基づいてデータロード
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
node_open = open('node.json', 'r')
node_load = json.load(node_open)
saved_open=open('saved.json','r') 

try:
    saved_load = json.load(saved_open)
except json.JSONDecodeError:
    print(f'Error: saved_load file is not found')
    saved_load=""
newsavefile = ('saved.json')
new_save_contents = {}

# 進捗チェック
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('ready on')
    channel = client.get_channel(CHANNEL_ID)
    sendstr = "進捗チェックします。",googlespreadsheet
    await channel.send(sendstr)
    for key,value in node_load.items():
        dt_now = datetime.datetime.now()
        # print(value["user"])
        # print(value["title"])
        # print(saved_load[key]["hash"])
        urlData = requests.get(value["checkurl"]).content
        # print(urlData)
        time.sleep(5)
        m = hashlib.sha256()
        m.update(urlData)
        # print(m.hexdigest())
        datestr = dt_now.strftime('%Y%m%d %H%M')
        hash = m.hexdigest()
        if (( key in saved_load ) and ("hash" in saved_load[key] ) and ( hash == saved_load[key]["hash"])):
            save_node = {"hash":hash,"date": saved_load[key]["date"] }
            # print(value["user"],value["title"],saved_load[key]["date"],"進捗ありません")
            sendstr = "進捗ないです",saved_load[key]["date"],value["user"],value["title"]
            await channel.send(sendstr)
        else:
            save_node = {"hash":hash,"date": datestr }
            # print(value["user"],value["title"],datestr,"更新ありました")
            sendstr = "捗ってますね",datestr,value["user"],value["title"]
            await channel.send(sendstr)
        new_save_contents[key] = save_node
    # await channel.send('進捗どうですか')

    with open(newsavefile, mode="wt", encoding="utf-8" )as f:
         json.dump(new_save_contents,f,ensure_ascii=False,indent=2)

    await client.close()
client.run(TOKEN)
