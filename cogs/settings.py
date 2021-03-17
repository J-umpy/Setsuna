import discord
from discord.ext import commands
from discord.ext.commands import bot, MemberConverter, TextChannelConverter
import json
import tools
def dump():
  with open('config.json', 'w') as f:
    json.dump(tools.data, f, indent=4)
class Settings(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  
  #Calls on the reload function from tools.py
  @commands.command(aliases=['toolsrld', 'settingsreload'])
  async def configreload(self, ctx):
    try:
      tools.cfgreload()
    except:
      embed = tools.buildembed("Config Reload", "Config could not be reloaded, please redownload the bot data from [here](https://github.com/Jumpyvonvagabond/Setsuna/releases)")
      await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Config Reload", "Successfully reloaded\nIf errors persist, please redownload the bot data from [here](https://github.com/Jumpyvonvagabond/Setsuna/releases)")
      await ctx.send(embed=embed)
  
  # Adds a bot prefix
  @commands.command()
  async def prefix(self, ctx, prefix = None):
    if prefix != None:
      if ctx.message.author.guild_permissions.administrator:
        tools.data['prefix'].append(prefix)
        dump()
        embed = tools.buildembed("Prefix", f"The command prefix has been set to `{prefix}`")
        await ctx.send(embed=embed)
      else:
        embed = tools.buildembed("Prefix", "This command requires administrator server permissions")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Prefix", f"The command prefix for this server is `{prefix}`")
      await ctx.send(embed=embed)
    
    
  # @commands.command()
  # async def welcome(self, ctx, payload = None, *, message = None):
  #   if ctx.message.author.guild_permissions.manage_channels:
  #     if payload != None:
  #       if payload.lower() == "message":
  #         if message == None:
  #           embed = tools.buildembed("Welcome", "You didn't enter a welcome message")
  #           await ctx.message.send("You forgot to input a new welcome message!")
  #         else:
  #           tools.data['welcome']['message'] = message
  #           dump()
  #           embed = tools.buildembed("Welcome", "You Have Changed the Welcome Message")
  #           embed.add_field(name="It is Now", value=message)
  #           await ctx.send(embed=embed)
  #       elif payload.lower() == "channel":
  #         try:
  #           message = await TextChannelConverter().convert(ctx, (message[1]))
  #         except:
  #           embed = tools.buildembed("Welcome", "Invalid channel input")
  #           await ctx.send(embed=embed)
  #         else:
  #           tools.data['welcome']['channel'] = message.id
  #           dump()
  #           embed = tools.buildembed("Welcome", f"Channel has been changed to{message.mention}")
  #           await ctx.send(embed=embed)
  #       elif payload.lower() == "toggle":
  #         if tools.data['welcome']['enabled'] == False:
  #           tools.data['welcome']['enabled'] = True
  #           dump()
  #           embed = tools.buildembed("Welcome", "Welcome messages have been set to True")
  #           await ctx.send(embed=embed)
  #         else:
  #           tools.data['welcome']['enabled'] = False
  #           dump()
  #           embed = tools.buildembed("Welcome", "Welcome messages have been set to False")
  #           await ctx.send(embed=embed)
  #       else:
  #         embed = tools.buildembed("Welcome Info", f"Here is a list of options, and their current values for {ctx.guild.name}")
  #         embed.add_field(name="Welcome message", value=f"To make a custom welcome message, use '{ctx.prefix}welcome message [message]'\nTo ping the user who joined, say {{MENTION}} where you want them to be pinged\nTo say the name of the server, use {{SERVER}}", inline=False)
  #         embed.add_field(name="Channel", value=f"To change the welcome channel, use '{ctx.prefix}welcome channel [channel]'", inline=False)
  #         embed.add_field(name="Toggle", value=f"To toggle the welcome message on and off, use '{ctx.prefix}welcome toggle'\n", inline=False)
  #         await ctx.channel.send(embed=embed)
  #   else:
  #     embed = tools.buildembed("Welcome", "This command requires the manage channels permission")
  #     await ctx.send(embed=embed)
  
  @commands.command(aliases=['wf'])
  async def wordfilter(self, ctx, payload = None, *, word = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload != None:
        if payload.lower() == 'toggle':
          if tools.data['wordfilter'] == False:
            tools.data['wordfilter'] = True
            dump()
            embed = tools.buildembed("Word Filter", "Word Filter has been set to True")
            await ctx.send(embed=embed)
          else:
            tools.data['wordfilter'] = False
            dump()
            embed = tools.buildembed("Word Filter", "Word Filter has been set to False")
            await ctx.send(embed=embed)
        elif payload.lower() == 'remove':
          try:
            tools.data['bannedwords'].remove(word.lower())
            dump()
          except:
            embed = tools.buildembed("Word Filter", f"{word} could not be found in the words list")
            await ctx.send(embed=embed)
          else:
            embed = tools.buildembed("Word Filter", f"{word} has been successfully removed")
            await ctx.send(embed=embed)
        elif payload.lower() == 'list':
          embed = tools.buildembed("Word Filter", tools.data['bannedwords'])
          await ctx.send(embed=embed)
        elif payload.lower() == 'add':
          if len(tools.data['bannedwords']) < 10:
            if len(word) < 100:
              tools.data['bannedwords'].append(word.lower())
              dump()
              embed = tools.buildembed("Word Filter", f"{word} added successfully")
              await ctx.send(embed=embed)
        else:
          embed = tools.buildembed("Word Filter", f"invalid argument. For a list of arguments, use\n `{ctx.prefix}wordfilter`")
          await ctx.send(embed=embed)
      else:
        embed = tools.buildembed("Word Filter", "Info")
        embed.add_field(name="Toggle", value=f"To toggle the word filter on and off, use `{ctx.prefix}wordfilter toggle`", inline=False)
        embed.add_field(name="Add", value=f"To add a word to the filter, use `{ctx.prefix}wordfilter add [word]`\nYou can use a phrase or a word\nWords/phrases must be under 100 characters", inline=False)
        embed.add_field(name="Remove", value=f"To remove a word from the filter, use `{ctx.prefix}wordfilter remove [word]`", inline=False)
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Word Filter", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  
  # @commands.command(aliases=['pb'])
  # async def pineappleboard(self, ctx, payload = None, setting= None):
  #   if ctx.message.author.guild_permissions.manage_channels:
  #     if payload.lower() == 'toggle':
  #       if tools.data['pineappleboard']['enabled'] == False:
  #         tools.data['pineappleboard']['enabled'] = True
  #         embed = tools.buildembed("Pineappleboard", "Pineappleboard has been enabled")
  #         await ctx.send(embed=embed)
  #       else:
  #         tools.data['pineappleboard']['enabled'] = False
  #         embed = tools.buildembed("Pineappleboard", "Pineappleboard has been disabled")
  #         await ctx.send(embed=embed)
  #       dump()
  #     elif payload.lower() == 'count':
  #       try:
  #         int(setting)
  #       except:
  #         embed = tools.buildembed("Pineappleboard", "the command requires a number as the input")
  #         await ctx.send(embed=embed)
  #       else:
  #         tools.data['pineappleboard']['count'] = int(setting)
  #         dump()
  #         embed = tools.buildembed("Pineappleboard", f"Pineapple threshold changed to {setting}")
  #         await ctx.send(embed=embed)
  #     elif payload.lower() == 'channel':
  #       try:
  #         payload = await TextChannelConverter().convert(ctx, str(setting))
  #       except:
  #         embed = tools.buildembed("Pineappleboard", "Invalid text channel input")
  #         await ctx.send(embed=embed)
  #       else:
  #         tools.data['pineappleboard']['channel'] = setting.id
  #         dump()
  #         embed = tools.buildembed("Pineappleboard", f"Pineappleboard channel changed to {setting.mention}")
  #         await ctx.send(embed=embed)
  #     else:
  #       embed = tools.buildembed("Pineappleboard Settings", "Here's a list of settings")
  #       embed.add_field(name="Count", value=f"To change the number of pineapples required to get a message added to the board, use {ctx.prefix}pineappleboard count [number]", inline=False)
  #       embed.add_field(name="Channel", value=f"To change the channel that messages added to the board are sent to, use {ctx.prefix}pineappleboard channel [channel]", inline=False)
  #       embed.add_field(name="Toggle", value=f"To toggle the pineappleboard on and off, use {ctx.prefix}pineappleboard toggle", inline=False)
  #       await ctx.send(embed=embed)
  #   else:
  #     embed = tools.buildembed("Pineappleboard", "This command requires the manage channels permission")
  #     await ctx.send(embed=embed)

  # Log settings
  @commands.command()
  async def log(self, ctx, payload = None, setting = None, delmessagechan = None):
    if ctx.message.author.guild_permissions.manage_channels:
      #Changes the log channel
      if payload.lower() == 'channel':
        try:
          payload = await TextChannelConverter().convert(ctx, str(setting))
        except:
          embed = tools.buildembed("Log", "Invalid text channel input")
          await ctx.send(embed=embed)
        else:
          tools.data['logchannel'] = payload.id
          dump()
      # Enables, disables logging
      elif payload.lower() == 'toggle':
        if tools.data['log'] == False:
          tools.data['log'] = True
          dump()
          embed = tools.buildembed("Log", "Logging has been changed to True")
          await ctx.send(embed=embed)
        else:
          tools.data['log'] = False
          dump()
          embed = tools.buildembed("Log", "Logging has been changed to False")
          await ctx.send(embed=embed)
      # Changes the channel deleted messages are logged in
      elif payload.lower() == 'deletedmessages':
        try:
          delmessagechan = await TextChannelConverter().convert(ctx, str(delmessagechan))
        except:
          embed = tools.buildembed("Log", "Invalid text channel input")
          await ctx.send(embed=embed)
        else:
          tools.data['deletedmessageschannel'] = delmessagechan.id
          dump()
      else:
        embed = tools.buildembed("Log Settings", "Here's a list of log settings")
        embed.add_field(name="Channel", value=f"To change the channel used for logging, use {ctx.prefix}log channel [channel]")
        embed.add_field(name="Toggle", value=f"To toggle logging on and off, use {ctx.prefix}log toggle")
        embed.add_field(name="Deleted Messages", value=f"To change the deleted messages channel, use {ctx.prefix}log deletedmessages [channel]")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
    
  @commands.command(aliases=['mutedrole'])
  async def muterole(self, ctx, role: discord.Role):
    tools.data['mute'] = int(role.id)
    dump()
    embed = tools.buildembed("Mute Role", description="Successfully changed to "+role.name)
    await ctx.send(embed=embed)
  @muterole.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, commands.RoleNotFound) or isinstance(error, commands.MissingRequiredArgument):
      embed = tools.buildembed(title="Muted Role", description="You did not specify a valid role (name or ID, case sensitive)")
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Settings(bot))