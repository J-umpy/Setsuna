import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import MemberConverter
from discord.ext.commands import TextChannelConverter
import json
import cfg
def dump():
  with open('config.json', 'w') as f:
    json.dump(cfg.data, f, indent=4)
class Settings(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  @commands.command(aliases=['cfgrld', 'settingsreload'])
  async def configreload(self, ctx):
    try:
      cfg.reload()
    except:
      await ctx.send("Config could not be reloaded, please redownload the bot data")
    else:
      await ctx.send("Config successfully reloaded")

  @commands.command()
  async def prefix(self, ctx, prefix = None):
    if ctx.message.author.guild_permissions.administrator and prefix != None:
      cfg.data['prefix'] = prefix
      dump()
      await ctx.send(f"Prefix is now `{cfg.data['prefix']}`")
    else:
      if ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("Only admins can use this command")
      else:
        await ctx.send(f"The prefix for this server is {cfg.data['prefix'][0]}")
  
  @commands.command()
  async def owner(self, ctx, owner = None):
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
    
  @commands.command()
  async def welcome(self, ctx, *, message = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if message == None:
        embed = cfg.buildembed("Welcome Info", f"Here is a list of options, and their current values for {ctx.guild.name}")
        embed.add_field(name="Welcome message", value=f"To make a custom welcome message, use '{ctx.prefix}welcome message [message]'\nTo ping the user who joined, say {{MENTION}} where you want them to be pinged", inline=False)
        embed.add_field(name="Channel", value=f"To change the welcome channel, use '{ctx.prefix}welcome channel [channel]'", inline=False)
        embed.add_field(name="Toggle", value=f"To toggle the welcome message on and off, use '{ctx.prefix}welcome toggle'\n", inline=False)
        await ctx.channel.send(embed=embed)
      else:
        message = message.split(" ", 1)
        if message[0].lower() == "message":
          if len(message) == 1:
            await ctx.message.send("You forgot to input a new welcome message!")
          else:
            cfg.data['welcome']['message'] = message[1]
            dump()
        elif message[0].lower() == "channel":
          try:
            channel = await TextChannelConverter().convert(ctx, (message[1]))
          except:
            await ctx.send("Invalid channel input")
          else:
            cfg.data['welcome']['channel'] = channel.id
            dump()
        elif message[0].lower() == "toggle":
          if cfg.data['welcome']['enabled'] == False:
            cfg.data['welcome']['enabled'] = True
            dump()
            self.bot.reload_extension('cogs.utility')
          else:
            cfg.data['welcome']['enabled'] = False
            dump()
            cog = self.bot.get_cog('Utility')
            self.bot.remove_listener(cog.on_member_join)
    else:
      await ctx.send("This command requires the manage channels permission")
  
  @commands.command()
  async def wordfilter(self, ctx, *, word = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if word == None:
        embed = cfg.buildembed("Word Filter Info", "Here is a list of word filter settings")
        embed.add_field(name="Toggle", value=f"To toggle the word filter on and off, use '{ctx.prefix}wordfilter toggle'", inline=False)
        embed.add_field(name="Add", value=f"To add a word to the filter, use '{ctx.prefix}wordfilter add [word]\nYou can use a phrase in place of a word'", inline=False)
        await ctx.send(embed=embed)
      elif word.lower() == 'toggle':
        cog = self.bot.get_cog('Administration')
        if cfg.data['wordfilter'] == False:
          cfg.data['wordfilter'] = True
          self.bot.reload_extension('cogs.administration')
          dump()
        else:
          cfg.data['wordfilter'] = False
          self.bot.remove_listener(cog.on_message)
          dump()
      else:
        word = word.split(' ', 1)
        cfg.data['slurs'].append(word[1])
        dump()
    else:
      await ctx.send("This command requires the manage channels permission")
  
  @commands.command(aliases=['pb'])
  async def pineappleboard(self, ctx, *, payload = "e"):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload == 'toggle':
        if cfg.data['pineappleboard']['enabled'] == False:
          cfg.data['pineappleboard']['enabled'] = True
          self.bot.reload_extension('cogs.utility')
        else:
          cfg.data['pineappleboard']['enabled'] = False
          cog = self.bot.get_cog('Utility')
          self.bot.remove_listener(cog.on_reaction_add)
        dump()
      elif payload.split(" ", 1)[0].lower() == 'count':
        try:
          int(payload.split(" ", 1)[1])
        except:
          await ctx.send("The count must be a number!")
        else:
          cfg.data['pineappleboard']['count'] = int(payload.split(" ", 1)[1])
          dump()
      elif payload.split(" ", 1)[0].lower() == 'channel':
        try:
          payload = await TextChannelConverter().convert(ctx, str(payload.split(" ", 1)[1]))
        except:
          await ctx.send("Invalid channel input")
        else:
          cfg.data['pineappleboard']['channel'] = payload.id
          dump()
      else:
        embed = cfg.buildembed("Pineappleboard Settings", "Here's a list of settings")
        embed.add_field(name="Count", value=f"To change the number of pineapples required to get a message added to the board, use {ctx.prefix}pineappleboard count [number]", inline=False)
        embed.add_field(name="Channel", value=f"To change the channel that messages added to the board are sent to, use {ctx.prefix}pineappleboard channel [channel]", inline=False)
        embed.add_field(name="Toggle", value=f"To toggle the pineappleboard on and off, use {ctx.prefix}pineappleboard toggle", inline=False)
        await ctx.send(embed=embed)
    else:
      await ctx.send("This command requires the manage channels permission")

  @commands.command()
  async def log(self, ctx, *, payload = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload.split(" ", 1)[0].lower() == 'channel':
        try:
          payload = await TextChannelConverter().convert(ctx, str((payload.split(" ", 1)[1])))
        except:
          await ctx.send("Invalid channel input")
        else:
          cfg.data['logchannel'] = payload.id
          dump()
      elif payload.lower() == 'toggle':
        if cfg.data['log'] == False:
          cfg.data['log'] = True
          self.bot.reload_extension('cogs.utility')
          dump()
        else:
          cfg.data['log'] = False
          cog = self.bot.get_cog('Utility')
          self.bot.remove_listener(cog.on_raw_message_delete)
          self.bot.remove_listener(cog.on_member_ban)
          dump()
      elif payload.split(" ", 1)[0].lower() == 'deletedmessages':
        payload = payload.split(" ", 1)[1]
        try:
          payload = await TextChannelConverter().convert(ctx, str(payload))
        except:
          await ctx.send("Invalid channel input")
        else:
          cfg.data['deletedmessageschannel'] = payload.id
          dump()
      else:
        embed = cfg.buildembed("Log Settings", "Here's a list of log settings")
        embed.add_field(name="Channel", value=f"To change the channel used for logging, use {ctx.prefix}log channel [channel]")
        embed.add_field(name="Toggle", value=f"To toggle logging on and off, use {ctx.prefix}log toggle")
        embed.add_field(name="Deleted Messages", value=f"To change the deleted messages channel, use {ctx.prefix}log deletedmessages [channel]")
        await ctx.send(embed=embed)
    else:
      await ctx.send("This command requires the manage channels permission")

def setup(bot):
  bot.add_cog(Settings(bot))