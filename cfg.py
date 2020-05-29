import json
import discord
cogs = ['cogs.administration', 'cogs.utility', 'cogs.help', 'cogs.settings', 'cogs.fun']
with open('config.json') as f:
  data = json.loads(f.read())
async def reload():
  global data
  with open('config.json') as f:
    data = json.loads(f.read())
def buildembed(title = "Placeholder Title", description = "Placeholder Description", colour = discord.Colour.from_rgb(251, 217, 229)):
  embed = discord.Embed(title=title, description=description, colour=colour)
  return embed
