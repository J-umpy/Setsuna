import json
import discord
import os
with open('config.json') as f:
  data = json.loads(f.read())
#Fetches a list of cogs for use in the launcher and help command. Thank you to Neeko_iko for introducing me to the OS module <3
async def fetch_cogs():
  cogs = []
  files = os.listdir('./cogs')
  for i in files:
    if i.endswith('.py'):
      i = i.replace('.py', '')
      cogs.append(i)
  return cogs
#Closes and re-opens config.json, resyncing the data in the RAM with what's written to the disk
async def cfgreload():
  global data
  with open('config.json') as f:
    data = json.loads(f.read())
#An embed creator. It has default arguments so if I forget something an error isn't raised
def buildembed(title = "Placeholder Title", description = "Placeholder Description", colour = discord.Colour.from_rgb(251, 217, 229)):
  embed = discord.Embed(title=title, description=description, colour=colour)
  return embed