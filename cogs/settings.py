import discord
from discord.ext import commands
from discord.ext.commands import bot, MemberConverter, TextChannelConverter
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
      embed = cfg.buildembed("Config Reload", "Config could not be reloaded, please redownload the bot data from [here](https://github.com/Jumpyvonvagabond/Setsuna/releases)")
      await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed("Config Reload", "Successfully reloaded\nIf errors persist, please redownload the bot data from [here](https://github.com/Jumpyvonvagabond/Setsuna/releases)")
      await ctx.send(embed=embed)

  @commands.command()
  async def prefix(self, ctx, prefix = None):
    if prefix != None:
      if ctx.message.author.guild_permissions.administrator:
        cfg.data['prefix'] = prefix
        dump()
        embed = cfg.buildembed("Prefix", f"The command prefix has been set to `{prefix}`")
        await ctx.send(embed=embed)
      else:
        embed = cfg.buildembed("Prefix", "This command requires administrator server permissions")
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed("Prefix", f"The command prefix for this server is `{prefix}`")
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
    
  @commands.command()
  async def welcome(self, ctx, payload = None, *, message = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload != None:
        if payload.lower() == "message":
          if message == None:
            embed = cfg.buildembed("Welcome", "You didn't enter a welcome message")
            await ctx.message.send("You forgot to input a new welcome message!")
          else:
            cfg.data['welcome']['message'] = message
            dump()
            embed = cfg.buildembed("Welcome", "You Have Changed the Welcome Message")
            embed.add_field(name="It is Now", value=message)
            await ctx.send(embed=embed)
        elif payload.lower() == "channel":
          try:
            message = await TextChannelConverter().convert(ctx, (message[1]))
          except:
            embed = cfg.buildembed("Welcome", "Invalid channel input")
            await ctx.send(embed=embed)
          else:
            cfg.data['welcome']['channel'] = message.id
            dump()
            embed = cfg.buildembed("Welcome", f"Channel has been changed to{message.mention}")
            await ctx.send(embed=embed)
        elif payload.lower() == "toggle":
          if cfg.data['welcome']['enabled'] == False:
            cfg.data['welcome']['enabled'] = True
            dump()
            self.bot.reload_extension('cogs.utility')
            embed = cfg.buildembed("Welcome", "Welcome messages have been set to True")
            await ctx.send(embed=embed)
          else:
            cfg.data['welcome']['enabled'] = False
            dump()
            cog = self.bot.get_cog('Utility')
            self.bot.remove_listener(cog.on_member_join)
            embed = cfg.buildembed("Welcome", "Welcome messages have been set to False")
            await ctx.send(embed=embed)
        else:
          embed = cfg.buildembed("Welcome Info", f"Here is a list of options, and their current values for {ctx.guild.name}")
          embed.add_field(name="Welcome message", value=f"To make a custom welcome message, use '{ctx.prefix}welcome message [message]'\nTo ping the user who joined, say {{MENTION}} where you want them to be pinged\nTo say the name of the server, use {{SERVER}}", inline=False)
          embed.add_field(name="Channel", value=f"To change the welcome channel, use '{ctx.prefix}welcome channel [channel]'", inline=False)
          embed.add_field(name="Toggle", value=f"To toggle the welcome message on and off, use '{ctx.prefix}welcome toggle'\n", inline=False)
          await ctx.channel.send(embed=embed)
    else:
      embed = cfg.buildembed("Welcome", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  
  @commands.command(aliases=['wf'])
  async def wordfilter(self, ctx, payload = None, *, word = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload != None:
        if payload.lower() == 'toggle':
          cog = self.bot.get_cog('Administration')
          if cfg.data['wordfilter'] == False:
            cfg.data['wordfilter'] = True
            self.bot.reload_extension('cogs.administration')
            dump()
            embed = cfg.buildembed("Word Filter", "Word Filter has been set to True")
            await ctx.send(embed=embed)
          else:
            cfg.data['wordfilter'] = False
            self.bot.remove_listener(cog.on_message)
            dump()
            embed = cfg.buildembed("Word Filter", "Word Filter has been set to False")
            await ctx.send(embed=embed)
        elif payload.lower() == 'remove':
          try:
            cfg.data['slurs'].remove(word.lower())
            dump()
          except:
            embed = cfg.buildembed("Word Filter", f"{word} could not be found in the words list")
            await ctx.send(embed=embed)
          else:
            embed = cfg.buildembed("Word Filter", f"{word} has been successfully removed")
            await ctx.send(embed=embed)
        elif payload.lower() == 'list':
          embed = cfg.buildembed("Word Filter", cfg.data['slurs'])
          await ctx.send(embed=embed)
        elif payload.lower() == 'add':
          if len(cfg.data['slurs']) < 10:
            if len(word) < 100:
              cfg.data['slurs'].append(word.lower())
              dump()
              embed = cfg.buildembed("Word Filter", f"{word} added successfully")
              await ctx.send(embed=embed)
        else:
          embed = cfg.buildembed("Word Filter", f"invalid argument. For a list of arguments, use\n `{ctx.prefix}wordfilter`")
          await ctx.send(embed=embed)
      else:
        embed = cfg.buildembed("Word Filter", "Info")
        embed.add_field(name="Toggle", value=f"To toggle the word filter on and off, use `{ctx.prefix}wordfilter toggle`", inline=False)
        embed.add_field(name="Add", value=f"To add a word to the filter, use `{ctx.prefix}wordfilter add [word]`\nYou can use a phrase or a word\nWords/phrases must be under 100 characters", inline=False)
        embed.add_field(name="Remove", value=f"To remove a word from the filter, use `{ctx.prefix}wordfilter remove [word]`", inline=False)
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed("Word Filter", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  
  @commands.command(aliases=['pb'])
  async def pineappleboard(self, ctx, payload = None, setting= None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload.lower() == 'toggle':
        if cfg.data['pineappleboard']['enabled'] == False:
          cfg.data['pineappleboard']['enabled'] = True
          self.bot.reload_extension('cogs.utility')
          embed = cfg.buildembed("Pineappleboard", "Pineappleboard has been enabled")
          await ctx.send(embed=embed)
        else:
          cfg.data['pineappleboard']['enabled'] = False
          cog = self.bot.get_cog('Utility')
          self.bot.remove_listener(cog.on_raw_reaction_add)
          embed = cfg.buildembed("Pineappleboard", "Pineappleboard has been disabled")
          await ctx.send(embed=embed)
        dump()
          
      elif payload.lower() == 'count':
        try:
          int(setting)
        except:
          embed = cfg.buildembed("Pineappleboard", "the command requires a number as the input")
          await ctx.send(embed=embed)
        else:
          cfg.data['pineappleboard']['count'] = int(setting)
          dump()
          embed = cfg.buildembed("Pineappleboard", f"Pineapple threshold changed to {setting}")
          await ctx.send(embed=embed)
      elif payload.lower() == 'channel':
        try:
          payload = await TextChannelConverter().convert(ctx, str(setting))
        except:
          embed = cfg.buildembed("Pineappleboard", "Invalid text channel input")
          await ctx.send(embed=embed)
        else:
          cfg.data['pineappleboard']['channel'] = setting.id
          dump()
          embed = cfg.buildembed("Pineappleboard", f"Pineappleboard channel changed to {setting.mention}")
          await ctx.send(embed=embed)
      else:
        embed = cfg.buildembed("Pineappleboard Settings", "Here's a list of settings")
        embed.add_field(name="Count", value=f"To change the number of pineapples required to get a message added to the board, use {ctx.prefix}pineappleboard count [number]", inline=False)
        embed.add_field(name="Channel", value=f"To change the channel that messages added to the board are sent to, use {ctx.prefix}pineappleboard channel [channel]", inline=False)
        embed.add_field(name="Toggle", value=f"To toggle the pineappleboard on and off, use {ctx.prefix}pineappleboard toggle", inline=False)
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed("Pineappleboard", "This command requires the manage channels permission")
      await ctx.send(embed=embed)

  @commands.command()
  async def log(self, ctx, payload = None, setting = None, delmessagechan = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload.lower() == 'channel':
        try:
          payload = await TextChannelConverter().convert(ctx, str(setting))
        except:
          embed = cfg.buildembed("Log", "Invalid text channel input")
          await ctx.send(embed=embed)
        else:
          cfg.data['logchannel'] = payload.id
          dump()
      elif payload.lower() == 'toggle':
        if cfg.data['log'] == False:
          cfg.data['log'] = True
          self.bot.reload_extension('cogs.utility')
          dump()
          embed = cfg.buildembed("Log", "Logging has been changed to True")
          await ctx.send(embed=embed)
        else:
          cfg.data['log'] = False
          cog = self.bot.get_cog('Utility')
          self.bot.remove_listener(cog.on_raw_message_delete)
          self.bot.remove_listener(cog.on_member_ban)
          dump()
          embed = cfg.buildembed("Log", "Logging has been changed to False")
          await ctx.send(embed=embed)
      elif payload.lower() == 'deletedmessages':
        try:
          delmessagechan = await TextChannelConverter().convert(ctx, str(delmessagechan))
        except:
          embed = cfg.buildembed("Log", "Invalid text channel input")
          await ctx.send(embed=embed)
        else:
          cfg.data['deletedmessageschannel'] = delmessagechan.id
          dump()
      else:
        embed = cfg.buildembed("Log Settings", "Here's a list of log settings")
        embed.add_field(name="Channel", value=f"To change the channel used for logging, use {ctx.prefix}log channel [channel]")
        embed.add_field(name="Toggle", value=f"To toggle logging on and off, use {ctx.prefix}log toggle")
        embed.add_field(name="Deleted Messages", value=f"To change the deleted messages channel, use {ctx.prefix}log deletedmessages [channel]")
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Settings(bot))