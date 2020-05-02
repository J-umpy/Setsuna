import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import MemberConverter
import json
import cfg
class Administration(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['b'])
  async def ban(self, ctx, member = None, reason = None):
    if ctx.message.author.guild_permissions.ban_members == False: 
      await ctx.channel.send("You don't have permission to ban people.")
    else:
      try:
        member = await MemberConverter().convert(ctx, member)
        author = await MemberConverter().convert(ctx, ctx.message.author.mention)
      except:
        await ctx.send("I couldn't find the user you wanted to ban!")
      else:
        if member == ctx.message.author:
          await ctx.send("Why would you try to ban yourself?")
        elif member.top_role >= author.top_role:
          await ctx.send("You can't ban that person! They're way better than you")
        else:
          if reason == None:
            await ctx.send("You forgot to input a ban reason!")
          elif len(reason) > 950:
            await ctx.send("The ban reason is too long")
          else:
            try:
              reason = ctx.message.content[len(cfg.data["prefix"]) + len(ctx.invoked_with) + len(member.mention) + 1:]
              embedreason = f' Was banned with reason: {reason} ||| Ban issued by {str(author)}'
              embed = discord.Embed(title = f"{str(member)} Was Banned", description = embedreason, colour=discord.Colour.blue())
              await ctx.send(embed=embed)
              await ctx.guild.ban(member, reason=reason, delete_message_days=0)
            except:
              await ctx.send("Missing permissions")

  @commands.command(aliases=['k'])
  async def kick(self, ctx, member = None, reason = None):
    if ctx.message.author.guild_permissions.kick_members == False: 
      await ctx.channel.send("You don't have permission to kick people.")
    else:
      try:
        member = await UserConverter().convert(ctx, member)
        author = await MemberConverter().convert(ctx, ctx.message.author.mention)
      except:
        await ctx.send("I couldn't find the user you wanted to kick!")
      else:
        if member == ctx.message.author:
          await ctx.channel.send("Don't kick yourself :(")
        elif member.top_role >= author.top_role:
          await ctx.send("You can't kick that person, their roles are cooler than yours")
        else:
          if reason == None:
            await ctx.channel.send("You forgot to input a reason!")
          elif len(reason) > 950:
            await ctx.send("The reason is too long")
          else:
            try:
              reason = ctx.message.content[len(cfg.data["prefix"]) + len(ctx.invoked_with) + len(member.mention) + 1:]
              embedreason = f' Was kicked with reason: {reason} ||| Issued by {str(author)}'
              embed = discord.Embed(title = f"{str(member)} Was Kicked", description = embedreason, colour=discord.Colour.blue())
              await ctx.channel.send(embed=embed)
              await ctx.guild.kick(member, reason=reason)
            except:
              await ctx.channel.send("I couldn't find the user you wanted to kick!")

  @commands.command(aliases=['purge'])
  async def clear(self, ctx, number = 5, member = None):
    if ctx.message.author.guild_permissions.manage_messages == False:
      await ctx.channel.send("The mods will yell at me if I listen to you...")
    try:
      int(number)
    except:
      await ctx.send('Please specify a number of messages')
    else:
      if number > 100:
        number = 100
      if member == None:
        await ctx.channel.purge(limit=int(number))
        channel = self.bot.get_channel(int(cfg.data['logchannel']))
        await channel.send(f"{ctx.message.author} cleared {number} messages in {ctx.channel.mention}")
      else:
        try:
          member = await UserConverter().convert(ctx, member)
        except:
          await ctx.send("I couldn't find the bad person, so I didn't delete any messages")
        else:
          def check(m):
            return m.author == member
          await ctx.purge(limit=int(number), check=check)
          channel = self.bot.get_channel(int(cfg.data['logchannel']))
          await channel.send(f"{ctx.message.author} cleared {number} messages in {ctx.channel.mention}")

  @commands.Cog.listener()
  async def on_message(self, message):
    if cfg.data["wordfilter"] == False:
      self.bot.remove_listener(Administration.on_message)
    else:
      if any(slur in message.content.lower() for slur in cfg.data['slurs']):
        await message.delete()
        channel = self.bot.get_channel(int(cfg.data['logchannel']))
        embed = discord.Embed(title=f"{message.author} used a slur", description=f"in {message.channel.mention}")
        await channel.send(embed=embed)
        await message.channel.send(f"{message.author.mention} don't say that word! This is a warning.")

def setup(bot):
  bot.add_cog(Administration(bot))