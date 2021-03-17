print("Booting Setsuna.....")

import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import tools
#Required as of Version 1.5 to tell Discord what events to subscribe to, default() is all
intents = discord.Intents.default()

#Grabs prefixes from the list in config.json and allows Setsuna to respond to commands when pinged
def get_prefix(client, message):
  prefixes = tools.data['prefixes']
  return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=tools.data['owner'])

#Discord.py comes with a help command, it's removed here so I can use a custom one
bot.remove_command("help")

#Prints a message in the console when Setsuna has successfully started up
@bot.event
async def on_ready():
  for extension in await tools.fetch_cogs():
    extension = "cogs."+extension
    bot.load_extension(extension)
  print("Boot success!")


bot.run(tools.data['token'])
