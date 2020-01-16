import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
with open('config.json') as f:
  data = json.loads(f.read())

if data["config"] == "false":
  setupresp = input("The bot has not been configured yet.\n\nRunning setup...\nPress Enter to begin setup\n")
  import configuration
  configuration.configurate()

bot = commands.Bot(command_prefix=data["prefix"])

@bot.event
async def on_ready():
  print("Connected")

@bot.event
async def on_member_join(member):
  general = bot.get_channel(data["generalchannel"])
  welcomemessage = "Welcome, "+member.mention+"! Come join us in "+general.mention
  embed = discord.Embed(title = "Welcome", description = welcomemessage, colour=discord.Colour.blue())
  embed.set_footer(text="We're glad to have you")
  embed.set_image(url=data["welcomeimage"])
  channel = bot.get_channel(data["welcomechannel"])
  await channel.send(embed=embed)























bot.run(data["token"])