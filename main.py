import os
import discord
import requests 
import json
import random
from replit import db
from keep_alive import keep_alive

intent = discord.Intents.default()
client = discord.Client(intents=intent)

sad_words=['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing', 'depression', 'lonely', 'heartbroken', 'gloomy', 'sorrow',]

starter_encouragements=['You are a great person', 'Stay strong', 'Keep going', 'You have got this', 'Believe in yourself', 'Keep pushing', 'You can do it', 'Keep smiling', 'Stay positive',]

if 'responding' not in db.keys():
  db['responding']=True

def get_quote():
  response=requests.get('https://zenquotes.io/api/random')
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] + "  -" + json_data[0]['a']
  return (quote)

def update_encouragements(encouraging_message):  
  if 'encouragements' in db.keys():  
      encouragements = db['encouragements']  
      encouragements.append(encouraging_message)  
      db['encouragements'] = encouragements
  else:  
      db['encouragements'] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db['encouragements']
  if len(encouragements)>index:
    del encouragements[index]
    db['encouragements '] = encouragements
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    
    if msg.lower().startswith('quote'):
      quotee = get_quote()
      await message.channel.send(quotee)

    if db['responding']:
      options = starter_encouragements
      if 'encouragements' in db.keys():
        options = options + list(db['encouragements'])
  
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.lower().startswith('new'):
      encouraging_message = msg.split('new',1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send('New encouraging message added.')

    if msg.lower().startswith('del'):
      encouragements = []
      if 'encouragements' in db.keys():
        index = int(msg.split('del',1)[1])
        delete_encouragement(index)
        encouragements = db['encouragements']
        await message.channel.send(encouragements)

    if msg.lower().startswith('list'):
      encouragements = []
      if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        await message.channel.send(encouragements)

    if msg.lower().startswith('responding'):
      value = msg.split('responding ',1)[1]
      
      if value.lower() == 'true':
        db['responding'] = True
        await message.channel.send('Responding is on.')

      else:
          db['responding'] = False
          await message.channel.send('Responding is off.')


keep_alive()
token=os.environ['TOKEN']
client.run(token)