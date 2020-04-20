import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import UserConverter
import json
with open('config.json') as f:
  data = json.loads(f.read())
slurs = ['nigger', 'faggot', 'fag', 'nigga', 'tranny', 'trannies', 'kike', 'dyke', 'poofta']
minislurs = ['whore', 'slut', 'retard', 'cunt']
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
  @commands.Cog.listener()
  async def on_message(self, message):
    if any(slur in message.content.lower() for slur in slurs):
      await message.delete()
      channel = self.bot.get_channel(int(data['logchannel']))
      await channel.send(f'{message.author} sent a slur in {message.channel}!')
      await message.channel.send(f"{message.author.mention} don't say that word! This is a warning.")
    if any(slur in message.content.lower() for slur in minislurs):
      await message.delete()
      channel = self.bot.get_channel(int(data['logchannel']))
      await channel.send(f'{message.author} sent a minislur in {message.channel}!')
      await message.channel.send("Hey! One of the words in your message contained a banned word. Usage of this word will result in punishment starting on 4.30.20")




def setup(bot):
  bot.add_cog(Administration(bot))