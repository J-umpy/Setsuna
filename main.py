import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import cfg
if cfg.data["config"] != True:
  def configurate():
    token = input("Enter Bot Token\n")
    cfg.data["token"] = token
    ownerid = input("Please enter your Discord ID")
    cfg.data["ownerid"] = ownerid
    with open('config.json', 'w') as f:
      json.dump(cfg.data, f)
    print("If you believe you've made a mistake, please redownload config.json")
  configurate()
def get_prefix(client, message):
  prefixes = [cfg.data['prefix']]
  return commands.when_mentioned_or(*prefixes)(client, message)
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command("help")
@bot.event
async def on_ready():
  print("\n\n\nConnected\n\n\n")
  for extension in cfg.cogs:
    bot.load_extension(extension)
bot.run(cfg.data["token"])
