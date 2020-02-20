import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import UserConverter
import json
with open('config.json') as f:
  data = json.loads(f.read())
class Administration(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ban(self, ctx, member = None, reason = None):
    if ctx.message.author.guild_permissions.ban_members == False: 
      await ctx.channel.send("You don't have permission to ban people.")
    else:
      try:
        member = await UserConverter().convert(ctx, member)
      except:
        print("\nError in command: Ban:\nUser not found, or no user was specified")
      if member == ctx.message.author:
        await ctx.channel.send("Why would you try to ban yourself?")
      else:
        if reason == None:
          await ctx.channel.send("You forgot to input a ban reason!")
        else:
          try:
            reason = ctx.message.content[len(data["prefix"]) + len(ctx.invoked_with) + len(member.mention) + 1:]
            embedreason = f' Was banned with reason: {reason}'
            embed = discord.Embed(title = "A User Was Banned", description = embedreason, colour=discord.Colour.blue())
            await ctx.channel.send(embed=embed)
            await ctx.guild.ban(member, reason=reason, delete_message_days=0)
          except:
            await ctx.channel.send("I couldn't find the user you wanted to ban!")
  @commands.command()
  async def kick(self, ctx, member = None, reason = None):
    if ctx.message.author.guild_permissions.kick_members == False: 
      await ctx.channel.send("You don't have permission to kick people.")
    else:
      try:
        member = await UserConverter().convert(ctx, member)
      except:
        print("\nError in command: Kick:\nUser not found, or no user was specified")
      if member == ctx.message.author:
        await ctx.channel.send("Don't kick yourself :(")
      else:
        if reason == None:
          await ctx.channel.send("You forgot to input a reason!")
        else:
          try:
            reason = ctx.message.content[len(data["prefix"]) + len(ctx.invoked_with) + len(member.mention) + 1:]
            embedreason = f' Was kicked with reason: {reason}'
            embed = discord.Embed(title = "A User Was Kicked", description = embedreason, colour=discord.Colour.blue())
            await ctx.channel.send(embed=embed)
            await ctx.guild.kick(member, reason=reason)
          except:
            await ctx.channel.send("I couldn't find the user you wanted to kick!")

def setup(bot):
  bot.add_cog(Administration(bot))