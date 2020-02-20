import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import MemberConverter
import json
with open('config.json') as f:
  data = json.loads(f.read())
if data["config"] == "false":
  setupresp = input("The bot has not been configured yet.\n\nRunning setup...\nPress Enter to begin setup\n")
  import configuration
  configuration.configurate()
bot = commands.Bot(command_prefix=data["prefix"])
cogs = ['cogs.administration', 'cogs.utility']
@bot.event
async def on_ready():
  print("Connected")
  for extension in cogs:
    bot.load_extension(extension)
bot.run(data["token"])
