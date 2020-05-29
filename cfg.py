import json
import discord
cogs = ['cogs.administration', 'cogs.utility', 'cogs.help', 'cogs.settings', 'cogs.fun']
def buildembed(title = "Placeholder Title", description = "Placeholder Description", colour = discord.Colour.from_rgb(251, 217, 229)):
  embed = discord.Embed(title=title, description=description, colour=colour)
  return embed