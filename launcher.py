print("Booting Setsuna.....")

import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import tools
import sqlite3
#Required as of Version 1.5 to tell Discord what events to subscribe to, default() is all
intents = discord.Intents.default()
intents.members = True
intents.presences = True

#Grabs prefixes from the list in config.json and allows Setsuna to respond to commands when pinged
def get_prefix(client, message):
  tools.cursor.execute("SELECT Prefix FROM GuildConfig WHERE GuildID='"+str(message.guild.id)+"'")
  prefix = tools.cursor.fetchall()
  try:
    prefix = prefix[0][0]
  except:
    prefix = '.'
  if prefix == None:
    prefix = '.'
  return commands.when_mentioned_or(prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=tools.data['owner'], intents=intents)

#Discord.py comes with a help command, it's removed here so I can use a custom one
bot.remove_command("help")

#Prints a message in the console when Setsuna has successfully started up
@bot.event
async def on_ready():
  for extension in await tools.fetch_cogs():
    extension = "cogs."+extension
    bot.load_extension(extension)
  await tools.deploy()
  print("Boot success!")


  @bot.check
  async def check_commands(ctx):
    bchannels = await tools.read("CommandBlocklist", "Channel", ctx.guild.id)
    bchannel = [''.join(i) for i in bchannels]
    return not ctx.channel.id in bchannel

@bot.event
async def on_guild_join(guild):
  properties = (guild.id, '.', 0, 0)
  tools.cursor.execute("INSERT INTO GuildConfig(GuildID, Prefix, TimeOutRole, XPEnabled) VALUES(?, ?, ?, ?)", properties)
  #tools.cursor.execute("INSERT INTO XP(GuildID, Member, ID, Count) VALUES(?, ?, ?, ?)", properties)
  properties = (guild.id, 0, 0, 0, 0, 0, 0)
  tools.cursor.execute("INSERT INTO Log(GuildID, DelMsg, Ban, Kick, Clear, Timeout, WordFilter) VALUES(?, ?, ?, ?, ?, ?, ?)", properties)
  tools.db.commit()
  tools.pending[guild.id] = {}

bot.run(tools.data['token'])
