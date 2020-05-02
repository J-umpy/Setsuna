import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import cfg
if cfg.data["config"] != True:
  token = input("Enter Bot Token\n")
  ownerid = input("Please enter your Discord ID")
  def configurate():
    cfgdata = {
      'prefix': '.',
      'token': token,
      'ownerid': [ownerid],
      'config': True,
      'swearfilter': False,
      'slurs': [],
      }
    with open('config.json', 'w') as f:
      json.dump(cfgdata, f)
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