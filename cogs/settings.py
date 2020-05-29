import discord
from discord.ext import commands
from discord.ext.commands import bot, MemberConverter, TextChannelConverter
import json
import cfg
import sdb
def dump():
  with open('config.json', 'w') as f:
    json.dump(cfg.data, f, indent=4)
class Settings(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  @commands.command()
  async def prefix(self, ctx, prefix = None):
    if prefix != None:
      if ctx.message.author.guild_permissions.manage_channels:
        await sdb.update('GuildConfig', 'Prefix', prefix, ctx.guild.id)
        embed = cfg.buildembed("Prefix", f"The command prefix has been set to `{prefix}`")
        await ctx.send(embed=embed)
      else:
        embed = cfg.buildembed("Prefix", "This command requires the manage channels server permission")
        await ctx.send(embed=embed)
    else:
      sdb.cursor.execute("SELECT Prefix FROM GuildConfig WHERE GuildID='"+str(ctx.guild.id)+"'")
      prefix = sdb.cursor.fetchall()
      embed = cfg.buildembed("Prefix", f"The command prefix for this server is `{prefix[0][0]}`")
      await ctx.send(embed=embed)
    
  @commands.command()
  async def botowner(self, ctx, owner = None):
    async def listowners(ctx, owner):
      embed = discord.Embed(title="List of Owners", description=ctx.guild.name, colour=discord.Colour.blue())
      counter = 0
      while counter < 10:
        for owner in cfg.data["ownerid"]:
          counter += 1
          try:
            member = await MemberConverter().convert(ctx, str(owner))
          except:
            embed.add_field(name=f'Owner: {owner}', value='Not a member of this server', inline=False)
          else:
            embed.add_field(name=f'Owner: {owner}', value=str(member), inline=False)
        break
      pages = len(cfg.data['ownerid'])//10
      if pages < 1:
        pages = 1
      embed.set_footer(text=f'Page 1 of {pages}')
      await ctx.send(embed=embed)
    if any(identification in str(ctx.message.author.id) for identification in str(cfg.data["ownerid"])):
      try:
        member = await MemberConverter().convert(ctx, owner)
        cfg.data['ownerid'].append(member.id)
        dump()
        await listowners(ctx, owner)
      except:
        await listowners(ctx, owner)
    else:
      listowners(ctx, owner)
    
  @commands.group()
  async def welcome(self, ctx):
    if ctx.invoked_subcommand == None:
      await self.welchelp(ctx)
  
  @welcome.command()
  async def message(self, ctx, *, message = None):
    if ctx.author.guild_permissions.manage_channels:
      if message == None:
        embed = cfg.buildembed("Welcome", "You didn't enter a welcome message")
        await ctx.message.send("You forgot to input a new welcome message!")
      else:
        await sdb.update('GuildConfig', 'WelcomeMessage', message, ctx.guild.id)
        embed = cfg.buildembed("Welcome", "You have changed the welcome message")
        embed.add_field(name="It is Now", value=message)
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed('Welcome', 'This command requires the manage messages guild permission')
  
  @welcome.command(aliases=['channel'])
  async def ch(self, ctx, channel = None):
    if ctx.author.guild_permissions.manage_channels:
      try:
        channel = await TextChannelConverter().convert(ctx, channel)
      except:
        embed = cfg.buildembed("Welcome", "Invalid channel input")
        await ctx.send(embed=embed)
      else:
        await sdb.update('GuildConfig', 'WelcomeChannel', channel.id, ctx.guild.id)
        embed = cfg.buildembed("Welcome", f"Channel has been changed to {channel.mention}")
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed('Welcome', 'This command requires the manage messages guild permission')
      await ctx.send(embed=embed)
  
  @welcome.command()
  async def toggle(self, ctx, tog):
    if ctx.author.guild_permissions.manage_channels:
      if tog.lower() == 'off':
        await sdb.update('GuildConfig', 'Welcome', 0, ctx.guild.id)
        embed = cfg.buildembed("Welcome", "Welcome messages have been set to False")
      elif tog.lower() == 'on':
        await sdb.update('GuildConfig', 'Welcome', 1, ctx.guild.id)
        embed = cfg.buildembed("Welcome", "Welcome messages have been set to True")
      else:
        embed = cfg.buildembed('Welcome', 'Please use `on` or `off` to toggle')
    else:
      embed = cfg.buildembed('Welcome', 'This command requires the manage messages guild permission')
    await ctx.send(embed=embed)
  
  @commands.group(aliases=['pb'])
  async def pineappleboard(self, ctx):
    if ctx.invoked_subcommand == None:
      embed = cfg.buildembed("Pineappleboard Settings", "Here's a list of settings")
      embed.add_field(name="Count", value=f"To change the number of pineapples required to get a message added to the board, use {ctx.prefix}pineappleboard count [number]", inline=False)
      embed.add_field(name="Channel", value=f"To change the channel that messages added to the board are sent to, use {ctx.prefix}pineappleboard channel [channel]", inline=False)
      embed.add_field(name="Toggle", value=f"To toggle the pineappleboard on and off, use {ctx.prefix}pineappleboard toggle", inline=False)
      await ctx.send(embed=embed)
  
  @pineappleboard.command(aliases=['toggle'])
  async def tog(self, ctx, tog):
    if ctx.author.guild_permissions.manage_channels:
      if tog.lower() == 'off':
        await sdb.update('PBConfig', 'Enabled', 0, ctx.guild.id)
        embed = cfg.buildembed("Pineappleboard", "Pineappleboard has been set to False")
      elif tog.lower() == 'on':
        await sdb.update('PBConfig', 'Enabled', 1, ctx.guild.id)
        embed = cfg.buildembed('Pineappleboard', "Pineappleboard has been set to True")
      else:
        embed = cfg.buildembed('Pineappleboard', 'Please use `on` or `off` to toggle')
    else:
      embed = cfg.buildembed('Pineappleboard', 'This command requires the manage messages guild permission')
    await ctx.send(embed=embed)
  
  @pineappleboard.command()
  async def count(self, ctx, payload):
    if ctx.author.guild_permissions.manage_channels:
      try:
        int(payload)
      except:
        embed = cfg.buildembed("Pineappleboard", "the command requires a number as the input")
      else:
        await sdb.update('PBConfig', 'Count', payload, ctx.guild.id)
        embed = cfg.buildembed("Pineappleboard", f"Pineapple threshold changed to {payload}")
    else:
      embed = cfg.buildembed("Pineappleboard", "This command requires the manage channels permission")
    await ctx.send(embed=embed)
      
  @pineappleboard.command()
  async def channel(self, ctx, payload):
    if ctx.author.guild_permissions.manage_channels:
      try:
        payload = await TextChannelConverter().convert(ctx, payload)
      except:
        embed = cfg.buildembed("Pineappleboard", "Invalid text channel input")
      else:
        await sdb.update('PBConfig', 'Channel', payload.id, ctx.guild.id)
        embed = cfg.buildembed("Pineappleboard", f"Pineappleboard channel changed to {payload.mention}")
    else:
      embed = cfg.buildembed("Pineappleboard", "This command requires the manage channels permission")
    await ctx.send(embed=embed)

  @commands.command()
  async def log(self, ctx, option, payload):
    if ctx.message.author.guild_permissions.manage_channels:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        if payload == '0':
          await sdb.update("Log", option.title(), 0, ctx.guild.id)
          embed = cfg.buildembed("Log", "This event will no longer be logged")
        else:
          embed = cfg.buildembed("Log Settings", f"All of these are log events. To change the settings use:\n {ctx.prefix}log [event] [channel]\nTo turn off a setting, say '0' instead of a channel\nBan\nKick\nClear\nDelMsg")
      else:
        option = option.lower()
        if option == 'delmsg':
          option = 'DelMsg'
        await sdb.update("Log", option.title(), payload.id, ctx.guild.id)
        embed = cfg.buildembed('Log', f'This event will now be logged in {payload.mention}')
      await ctx.send(embed=embed)
  
  async def welchelp(self, ctx):
    embed = cfg.buildembed("Welcome Info", f"Here is a list of options, and their current values for {ctx.guild.name}")
    embed.add_field(name="Welcome message", value=f"To make a custom welcome message, use `{ctx.prefix}welcome message [message]`\nTo ping the user who joined, say {{MENTION}} where you want them to be pinged\nTo say the name of the server, use {{SERVER}}", inline=False)
    embed.add_field(name="Channel", value=f"To change the welcome channel, use `{ctx.prefix}welcome channel [channel]`\n", inline=False)
    embed.add_field(name="Toggle", value=f"To toggle the welcome message on and off, use `{ctx.prefix}welcome toggle`", inline=False)
    await ctx.channel.send(embed=embed)







def setup(bot):
  bot.add_cog(Settings(bot))