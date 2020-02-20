import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import MemberConverter
from discord.utils import get
import json
with open('config.json') as f:
  data = json.loads(f.read())
bot = commands.Bot(command_prefix=data["prefix"])

async def mention(ctx):
  role = ctx.message.content[len(data["prefix"]) + len(ctx.invoked_with) + 1:]
  try:
    role = get(ctx.guild.roles, name = role)
  except:
    await ctx.channel.send("Role not found")
  else:
    await ctx.channel.send("What channel would you like the mention in?")
    def check(m):
      return m.author == ctx.message.author and m.channel == ctx.message.channel
    msg = await bot.wait_for('message', check=check, timeout=30)
    await ctx.channel.send(msg.content)

    #try:
      #channel = get(ctx.guild.channels, name = sendin)
      #await role.edit(mentionable = True, reason = f"Called on by: {ctx.message.author}")
      #await ctx.channel.send(role.mention)
      #await role.edit(mentionable = False, reason = f"Called on by: {ctx.message.author}")
    #except:
      #await ctx.channel.send("Missing Permissions")