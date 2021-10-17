import discord
import os
from keep_alive import keep_alive
from replit import db
from discord.ext import tasks
from datetime import date, datetime


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    channel = client.get_channel(873501285482106940)
    print('channel', channel)
    change_status.start(channel)
    print('We have logged in as {0.user}'.format(client))

def get_all_entries():
  keys = db.keys()
  results = {}
  for key in keys:
    results[key] = db[key]
  return results






@tasks.loop(minutes=1)
async def change_status(channel):
  today = date.today().strftime("%d.%m")
  current_year = int(date.today().strftime("%Y"))
  # print(current_year)
  entries = get_all_entries()
  keys = entries.keys()
  now = datetime.now()
  # print(channel)
  current_time = now.strftime("%H:%M:%S")[:-3]
  print("Current Time =", current_time)
  # compare all bdays to today
  for key in keys:
    bday = entries[key]
    bday_year = int(bday[6:])
    age = current_year - bday_year
    bday_date = bday[:-5]
    if(today == bday_date):
      message = "Happy Birthday, " + "<@" + key + ">! \n"
      message += "Thanks for making the world a better place with your enormously large... \n \n"
      message += "|| heart <3 || \n \n"
      message += "We've already survived **" + str(age) + "** years with you on our planet. \n"
      message += "Hopefully there will be many more!"
      # print(message)
      print(current_time)
      if(current_time=="17:00"):
        await channel.send(message)
  # print('entries', entries)

  
  # await channel.send('hello')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bday setmy'):
        bday = message.content.split('$bday setmy ')[1]
        print(bday)
        db_key = str(message.author.id)
        db[db_key] = bday

        answer = 'I set the birthday for you, ' + message.author.name + '!'
        await message.channel.send(answer)

    if message.content.startswith('$bday setfor'):
      user = message.content.split('$bday setfor ')[1].split(' ')[0]
      bday = message.content.split('$bday setfor ')[1].split(' ')[1]
      print('user', user)
      print('bday', bday)
      db_key = user[3:len(user)-1]
      print('db_key', db_key)
      db[db_key] = bday

      answer = 'I set the birthday for ' + user + '!'
      await message.channel.send(answer)

    if message.content.startswith('$bday help'):
      answer='Here are all possible commands || friend ||: \n'
      answer += "> **$bday help**: list all possible commands \n"
      answer += "> **$bday setmy 01.01.2021**: sets your birthday to the date (dd.mm.yyyy) \n"
      answer += "> **$bday setfor @user 01.01.2021**: sets the birthday for a tagged user \n"
      answer += "> **$bday list **: list all birthdays"
      await message.channel.send(answer)

    if message.content.startswith('$bday list'):
      keys = db.keys()
      answer = 'All birthdays I know: \n'
      for user_id in keys:
        bday = db[user_id]
        answer += "<@" + user_id + ">: " + bday + "\n"

      print(answer)
      await message.channel.send(answer)



keep_alive()
client.run(os.getenv('TOKEN'))
