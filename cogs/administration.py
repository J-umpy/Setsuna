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
  async def ban(self, ctx, member = None, *, reason = None):
    if ctx.message.author.guild_permissions.ban_members == True:
      try:
        member = await MemberConverter().convert(ctx, member)
      except:
        embed = cfg.buildembed('Ban', "I couldn't find the person you are looking for")
        await ctx.send(embed=embed)
      else:
        if member == ctx.message.author:
          await ctx.send("Why would you try to ban yourself?")
        elif member.top_role >= ctx.message.author.top_role:
          await ctx.send(f"You can't ban {member.name}! They're way better than you")
        else:
          if reason == None:
            embed = cfg.buildembed('Ban', 'You forgot to input a ban reason!')
            await ctx.send(embed=embed)
          elif len(reason) > 460:
            embed = cfg.buildembed('Ban', 'The reason is too long!')
            await ctx.send(embed=embed)
          else:
            try:
              embed = cfg.buildembed('Ban', f'{str(member)} was banned by {str(ctx.message.author)}', discord.Colour.red())
              embed.add_field(name='Reason', value=reason)
              await ctx.send(embed=embed)
              await ctx.guild.ban(member, reason=f'{reason} ||| Ban issued by: {str(ctx.message.author)}', delete_message_days=0)
            except:
              embed = cfg.buildembed('Ban', 'I am missing permissions')
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
            embed = cfg.buildembed('Kick', 'You forgot to input a reason!')
            await ctx.send(embed=embed)
          elif len(reason) > 464:
            embed = cfg.buildembed('Kick', 'The reason is too long!')
            await ctx.send(embed=embed)
          else:
            try:
              embed = cfg.buildembed('Kick', f'{str(member)} was banned by {str(ctx.message.author)}', discord.Colour.red())
              embed.add_field(name='Reason', value=reason)
              await ctx.channel.send(embed=embed)
              await ctx.guild.kick(member, reason=f'{reason} ||| Kicked by: {str(ctx.message.author)}')
            except:
              embed = cfg.buildembed('Kick', 'I am missing permissions')
              await ctx.send(embed=embed)

  @commands.command(aliases=['purge'])
  async def clear(self, ctx, number = 5, member = None):
    if ctx.message.author.guild_permissions.manage_messages == True:
      try:
        int(number)
      except:
        embed = cfg.buildembed('Clear', 'This command requires a number of messages to be specified')
        await ctx.send(embed=embed)
      else:
        if number > 99:
          number = 99
        if member == None:
          await ctx.channel.purge(limit=(int(number)+1))
          channel = self.bot.get_channel(int(cfg.data['logchannel']))
          embed = cfg.buildembed(str(ctx.message.author), f'cleared {number} messages in {ctx.channel.mention}')
          await channel.send(embed=embed)
        else:
          try:
            member = await MemberConverter().convert(ctx, str(member))
          except:
            embed = cfg.buildembed('Clear', f"I couldn't find {str(member)}, so I didn't delete any messages")
            await ctx.send(embed=embed)
          else:
            def check(m):
              return m.author.id == member.id
            await ctx.channel.purge(limit=int(number), check=check)
            if cfg.data['log'] == True:
              channel = self.bot.get_channel(int(cfg.data['logchannel']))
              embed = cfg.buildembed(ctx.message.author, f'cleared {number} messages by {str(member)} in {ctx.channel.mention}')
              await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_message(self, message):
    if cfg.data['wordfilter'] == True:
      if any(slur in message.content.lower() for slur in cfg.data['slurs']):
        await message.delete()
        channel = self.bot.get_channel(int(cfg.data['logchannel']))
        embed = cfg.buildembed(f"{message.author} used a slur", f"in {message.channel.mention}")
        await channel.send(embed=embed)
        await message.channel.send(f"{message.author.mention} don't say that word! This is a warning.")

def setup(bot):
  bot.add_cog(Administration(bot))