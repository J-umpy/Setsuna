import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import cfg
import sdb
if cfg.data["config"] != True:
  def configurate():
    token = input("Enter Bot Token\n")
    cfg.data["token"] = token
    ownerid = input("Please enter your Discord ID")
    cfg.data["ownerid"] = ownerid
    with open('config.json', 'w') as f:
      json.dump(cfg.data, f)
    print("If you believe you've made a mistake, please open and edit config.json")
  configurate()


async def get_prefix(bot, message):
  sdb.cursor.execute("SELECT Prefix FROM GuildConfig WHERE GuildID='"+str(message.guild.id)+"'")
  prefix = sdb.cursor.fetchall()
  try:
    prefix = prefix[0][0]
  except:
    prefix = '.'
  if prefix == None:
    prefix = '.'
  return commands.when_mentioned_or(prefix)(bot, message)
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, help_command=None)

@bot.event
async def on_ready():
  print("\n\n\nConnected\n\n\n")
  for extension in cfg.cogs:
    bot.load_extension(extension)
    await sdb.deploy()
  

@bot.event
async def on_guild_join(guild):
  properties = (guild.id, '.', 0, 0, None)
  sdb.cursor.execute("INSERT INTO GuildConfig(GuildID, Prefix, Welcome, WelcomeChannel, WelcomeMessage) VALUES(?, ?, ?, ?, ?)", properties)
  properties = (guild.id, 0, None, 0)
  sdb.cursor.execute("INSERT INTO PBConfig(GuildID, Enabled, Channel, Count) VALUES(?, ?, ?, ?)", properties)
  properties = (guild.id, 0, 0, 0, 0)
  sdb.cursor.execute("INSERT INTO Log(GuildID, DelMsg, Ban, Kick, Clear) VALUES(?, ?, ?, ?, ?)", properties)
  sdb.db.commit()
bot.run(cfg.data["token"])
#https://discord.com/oauth2/authorize?client_id=