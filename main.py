import discord
import os
import praw
import random
from discord.ext import commands
from keep_alive import keep_alive

reddit = praw.Reddit(
    client_id=os.environ['publicID'],
    client_secret=os.environ['privateID'],
    user_agent= os.environ['userAgent']
)
bot = commands.Bot(command_prefix='!')

@bot.command()
async def memes(ctx,arg1="memes",arg2=3):
  subm = []
  if arg1.isdigit() :
    arg2 = int(arg1)
    arg1 = "dankmemes"
  try :
    subreddit =  reddit.subreddit(arg1)
    for submission in subreddit.hot(limit=50):
      subm.append(submission)
    for i in range(arg2) :
      random_sub = random.choice(subm)
      if random_sub.is_self == True and random_sub.selftext !=""  :
        string = random_sub.title + "\n" + random_sub.selftext
        await ctx.send(string)
      else :
        em = discord.Embed(title = random_sub.title)
        em.set_image(url = random_sub.url)
        await ctx.send(embed = em)
  except :
    await ctx.send("Subreddit not found or wrong number.")
    

@bot.command()
async def HamaHelp(ctx) :
  await ctx.send('''
  Greetings : Write "Hello hama"
  Memes : !memes [Optional: subreddit (Default=r/memes)] [Optional: Number (Default=3)]
    -- Exemple !memes dankmemes 5
  '''
  )



@bot.event
async def on_ready() :
  print("Client {} logged in ".format(bot.user))

@bot.listen('on_message')
async def reply(msg) :
  if msg.author == bot.user :
    return
  if msg.content.startswith("Hello hama") :
    await msg.channel.send('Greetings {}'.format(msg.author))

keep_alive()
bot.run(os.environ['token'])
