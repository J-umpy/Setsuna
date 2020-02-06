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

bot = commands.Bot(command_prefix=data["prefix"], case_insensitive=True)

@bot.event
async def on_ready():
  print("Connected")

@bot.event
async def on_member_join(member):
  general = bot.get_channel(int(data["generalchannel"]))
  welcomemessage = "Welcome, "+member.mention+"! Come join us in "+general.mention
  embed = discord.Embed(title = "Welcome", description = welcomemessage, colour=discord.Colour.blue())
  embed.set_footer(text="We're glad to have you")
  embed.set_image(url=data["welcomeimage"])
  channel = bot.get_channel(int(data["welcomechannel"]))
  await channel.send(embed=embed)


#Administration
@bot.command(aliases = ["b"])
async def ban(ctx, member = None, reason = None):
  import administration
  await administration.ban(ctx, member, reason)
@bot.command(aliases = ["k"])
async def kick(ctx, member = None, reason = None):
  import administration
  await administration.kick(ctx, member, reason)

#Utility
@bot.command(aliases = ["m"])
async def mention(ctx):
  import utility
  await utility.mention(ctx)


















bot.run(data["token"], reconnect = True)