import discord
import os
from dotenv import load_dotenv
import requests
import json
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!"
]

# Simulação do banco de dados com um dicionário Python
db = {
    "encouragements": starter_encouragements,
    "responding": True
}

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def update_encouragements(encouraging_message):
    encouragements = db.get("encouragements", [])
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements

def delete_encouragement(index):
    encouragements = db.get("encouragements", [])
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    if db["responding"]:
        options = starter_encouragements + db.get("encouragements", [])
        
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith('$new'):
        encouraging_message = msg.split('$new ', 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        index = int(msg.split("$del ", 1)[1])
        delete_encouragement(index)
        await message.channel.send("Encouraging message deleted.")

    if msg.startswith("$list"):
        encouragements = db.get("encouragements", [])
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1].strip().lower()

        if value == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

client.run(os.getenv('TOKEN'))
