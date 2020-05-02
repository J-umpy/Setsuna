import json
import discord
cogs = ['cogs.administration', 'cogs.utility', 'cogs.help', 'cogs.settings']
with open('config.json') as f:
  data = json.loads(f.read())
async def reload():
  global data
  with open('config.json') as f:
    data = json.loads(f.read())
def buildembed(title = "Placeholder Title", description = "Placeholder Description", colour = discord.Colour.blue()):
  embed = discord.Embed(title=title, description=description, colour=colour)
  return embed