import discord
from discord.ext import commands
from discord.ext.commands import bot, RoleConverter, MemberConverter
import json
import tools
import asyncio
class Administration(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['b', 'execute'])
  async def ban(self, ctx, member = None, *, reason = None):
    if ctx.author.guild_permissions.ban_members == True:
      try:
        member = await MemberConverter().convert(ctx, member)
      except:
        embed = tools.buildembed('Ban', "I couldn't find the person you are looking for")
        await ctx.send(embed=embed)
      else:
        if member == ctx.author:
          await ctx.send("Why would you try to ban yourself?")
        elif member.top_role >= ctx.author.top_role:
          await ctx.send(f"You can't ban {member.name}! They're way better than you")
        else:
          if reason == None:
            embed = tools.buildembed('Ban', 'You forgot to input a ban reason!')
            await ctx.send(embed=embed)
          elif len(reason) > 460:
            embed = tools.buildembed('Ban', 'The reason is too long! Ban reasons must be under 460 characters')
            await ctx.send(embed=embed)
          else:
            embed = tools.buildembed('Ban', f'{str(member)} was banned by {str(ctx.message.author)}', discord.Colour.red())
            embed.add_field(name='Reason', value=reason)
            await ctx.guild.ban(member, reason=f'{reason} ||| Ban issued by: {str(ctx.message.author)}', delete_message_days=0)
            await ctx.send(embed=embed)

  @commands.command(aliases=['k'])
  async def kick(self, ctx, member = None, *, reason = None):
    if ctx.author.guild_permissions.kick_members == True:
      try:
        member = await MemberConverter().convert(ctx, member)
      except:
        await ctx.send("Can't kick 'em if I can't find 'em")
      else:
        if member == ctx.author:
          await ctx.channel.send("Don't kick yourself :c")
        elif member.top_role >= ctx.author.top_role:
          await ctx.send(f"You can't kick {member.name}, their roles are way cooler than your roles")
        else:
          if reason == None:
            embed = tools.buildembed('Kick', 'You forgot to input a reason!')
            await ctx.send(embed=embed)
          elif len(reason) > 464:
            embed = tools.buildembed('Kick', 'The reason is too long! Kick reasons must be under 460 characters')
            await ctx.send(embed=embed)
          else:
            embed = tools.buildembed('Kick', f'{str(member)} was banned by {str(ctx.message.author)}', discord.Colour.red())
            embed.add_field(name='Reason', value=reason)
            await ctx.guild.kick(member, reason=f'{reason} ||| Kicked by: {str(ctx.message.author)}')
            await ctx.send(embed=embed)

  @commands.command(aliases=['purge', 'c', 'p'])
  async def clear(self, ctx, number = 5, member = None):
    if ctx.author.guild_permissions.manage_messages == True:
      try:
        int(number)
      except:
        embed = tools.buildembed('Clear', 'This command requires a number of messages to be specified')
        await ctx.send(embed=embed)
      else:
        if number > 99:
          number = 99
        channel = await tools.read("Log", "Clear", ctx.guild.id)
        channel = channel[0][0]
        if member == None:
          await ctx.channel.purge(limit=(int(number)+1))
          if channel != 0:
            channel = self.bot.get_channel(int(channel))
            embed = tools.buildembed(str(ctx.message.author), f'cleared {number} messages in {ctx.channel.mention}')
            await channel.send(embed=embed)
        else:
          member = await MemberConverter().convert(ctx, str(member))
          def check(m):
            return m.author.id == member.id
          await ctx.channel.purge(limit=int(number), check=check)
          if channel != 0:
            channel = self.bot.get_channel(int(channel))
            embed = tools.buildembed(ctx.message.author, f'cleared {number} messages by {str(member)} in {ctx.channel.mention}')
            await channel.send(embed=embed)
  
  @commands.command(aliases=['t'])
  async def timeout(self, ctx, member: discord.Member, *, reason = None):
    if ctx.author.guild_permissions.manage_roles:
      if reason == None:
        await ctx.send("You forgot to input a reason!")
      else:
        role = await tools.read("GuildConfig", "TimeOutRole", ctx.guild.id)
        role = role[0][0]
        if role == 0:
          embed = tools.buildembed("Timeout", "Choose a role to assign to users who are timed out")
          await ctx.send(embed=embed)
        def check(role):
          return role.channel == ctx.channel and role.author == ctx.author
        try:
          role = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
          embed = tools.buildembed('Timeout', "I got tired of waiting for you to say something. Try again later, alright?")
          await ctx.send(embed=embed)
        try:
          role = await RoleConverter().convert(ctx, role)
        except:
          embed = tools.buildembed("Timeout", "Invalid Role")
        else:
          await tools.update("GuildConfig", "TimeOutRole", role.id, ctx.guild.id)
          tools.db.commit()
          role = role.id
        role = ctx.guild.get_role(role)
        await member.add_roles(role, reason=reason)
        channel = await tools.read("Log", "Timeout", ctx.guild.id)
        channel = channel[0][0]
        channel = self.bot.get_channel(channel)
        embed = tools.buildembed("Timeout", f"{str(member)} is taking some time away from the chat with reason: {reason}")
        await channel.send(embed=embed)
  @timeout.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, discord.HTTPException):
      pass
  @timeout.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, discord.Forbidden):
      embed = tools.buildembed(ctx.command.qualified_name.title(), "I am missing the permissions required to perform this action")
      await ctx.send(embed=embed)
  @timeout.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.MissingRequiredArgument):
      embed = tools.buildembed(title="Muted Role", description="I couldn't find the member you're looking for (name or ID, case sensitive)")
      await ctx.send(embed=embed)

  # @commands.command(aliases=["vibecheck"])
  # async def namecheck
  @commands.Cog.listener()
  async def on_message(self, message):
    bword = await tools.read("WordFilter", "Word", message.guild.id)
    bwords = [''.join(i) for i in bword]
    if len(bwords) > 0:
      if any(word in message.content.lower() for word in bwords):
        await message.delete()
        channel = await tools.read("Log", "WordFilter", message.guild.id)
        channel = self.bot.get_channel(channel[0][0])
        if channel != None:
          embed = tools.buildembed(f"{message.author} used a banned word", f"in {message.channel.mention}\n Full message: ||{message.content}||")
          await channel.send(embed=embed)
          await message.channel.send(f"{message.author.mention} don't say that word! This is a warning.")

def setup(bot):
  bot.add_cog(Administration(bot))