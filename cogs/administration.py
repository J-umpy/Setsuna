import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import MemberConverter
import json
import tools
class Administration(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['b', 'execute'])
  async def ban(self, ctx, member = None, *, reason = None):
    if ctx.message.author.guild_permissions.ban_members == True:
      try:
        member = await MemberConverter().convert(ctx, member)
      except:
        embed = tools.buildembed('Ban', "I couldn't find the person you are looking for")
        await ctx.send(embed=embed)
      else:
        if member == ctx.message.author:
          await ctx.send("Why would you try to ban yourself?")
        elif member.top_role >= ctx.message.author.top_role:
          await ctx.send(f"You can't ban {member.name}! They're way better than you")
        else:
          if reason == None:
            embed = tools.buildembed('Ban', 'You forgot to input a ban reason!')
            await ctx.send(embed=embed)
          elif len(reason) > 460:
            embed = tools.buildembed('Ban', 'The reason is too long!')
            await ctx.send(embed=embed)
          else:
            embed = tools.buildembed('Ban', f'{str(member)} was banned by {str(ctx.message.author)}', discord.Colour.red())
            embed.add_field(name='Reason', value=reason)
            await ctx.guild.ban(member, reason=f'{reason} ||| Ban issued by: {str(ctx.message.author)}', delete_message_days=0)
            await ctx.send(embed=embed)

  @commands.command(aliases=['k'])
  async def kick(self, ctx, member = None, *, reason = None):
    if ctx.message.author.guild_permissions.kick_members == True:
      try:
        member = await UserConverter().convert(ctx, member)
      except:
        await ctx.send("Can't kick 'em if I can't find 'em")
      else:
        if member == ctx.message.author:
          await ctx.channel.send("Don't kick yourself :c")
        elif member.top_role >= ctx.message.author.top_role:
          await ctx.send(f"You can't kick {member.name}, their roles are way cooler than your roles")
        else:
          if reason == None:
            embed = tools.buildembed('Kick', 'You forgot to input a reason!')
            await ctx.send(embed=embed)
          elif len(reason) > 464:
            embed = tools.buildembed('Kick', 'The reason is too long!')
            await ctx.send(embed=embed)
          else:
            embed = tools.buildembed('Kick', f'{str(member)} was banned by {str(ctx.message.author)}', discord.Colour.red())
            embed.add_field(name='Reason', value=reason)
            await ctx.guild.kick(member, reason=f'{reason} ||| Kicked by: {str(ctx.message.author)}')
            await ctx.send(embed=embed)

  @commands.command(aliases=['purge'])
  async def clear(self, ctx, number = 5, member = None):
    if ctx.message.author.guild_permissions.manage_messages == True:
      try:
        int(number)
      except:
        embed = tools.buildembed('Clear', 'This command requires a number of messages to be specified')
        await ctx.send(embed=embed)
      else:
        if number > 99:
          number = 99
        if member == None:
          await ctx.channel.purge(limit=(int(number)+1))
          channel = self.bot.get_channel(int(tools.data['logchannel']))
          embed = tools.buildembed(str(ctx.message.author), f'cleared {number} messages in {ctx.channel.mention}')
          await channel.send(embed=embed)
        else:
          member = await MemberConverter().convert(ctx, str(member))
          def check(m):
            return m.author.id == member.id
          await ctx.channel.purge(limit=int(number), check=check)
          if tools.data['log'] == True:
            channel = self.bot.get_channel(int(tools.data['logchannel']))
            embed = tools.buildembed(ctx.message.author, f'cleared {number} messages by {str(member)} in {ctx.channel.mention}')
            await channel.send(embed=embed)
  
  @commands.command(aliases=['m'])
  async def mute(self, ctx, member = None, *, reason = None):
    if ctx.author.guild_permissions.manage_roles:
      if reason == None:
        await ctx.send("You forgot to input a reason!")
      else:
        member = await MemberConverter().convert(ctx, member)
        role = ctx.guild.get_role(tools.data['mute'])
        await member.add_roles(role, reason=reason)
        channel = self.bot.get_channel(tools.data['logchannel'])
        embed = cfg.buildembed("Muted", f"{str(member)} has been muted with reason: {reason}")
        await channel.send(embed=embed)
  @mute.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, discord.HTTPException):
      pass
  @mute.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, discord.Forbidden):
      embed = tools.buildembed(ctx.command.qualified_name.title(), "I am missing the permissions required to perform this action")
      await ctx.send(embed=embed)


  @commands.Cog.listener()
  async def on_message(self, message):
    if tools.data['wordfilter'] == True:
      if any(word in message.content.lower() for word in tools.data['bannedwords']):
        await message.delete()
        channel = self.bot.get_channel(int(tools.data['logchannel']))
        embed = tools.buildembed(f"{message.author} used a banned word", f"in {message.channel.mention}")
        await channel.send(embed=embed)
        await message.channel.send(f"{message.author.mention} don't say that word! This is a warning.")

def setup(bot):
  bot.add_cog(Administration(bot))