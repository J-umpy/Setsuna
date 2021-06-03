import discord
from discord.ext import commands
from discord.ext.commands import bot, MemberConverter, TextChannelConverter
import tools
class Settings(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  
  
  # Adds a bot prefix
  @commands.command()
  async def prefix(self, ctx, prefix = None):
    if prefix != None:
      if ctx.message.author.guild_permissions.manage_channels:
        await tools.update('GuildConfig', 'Prefix', prefix, ctx.guild.id)
        embed = tools.buildembed("Prefix", f"The command prefix has been set to `{prefix}`")
        await ctx.send(embed=embed)
      else:
        embed = tools.buildembed("Prefix", "This command requires the manage channels server permission")
        await ctx.send(embed=embed)
    else:
      tools.cursor.execute("SELECT Prefix FROM GuildConfig WHERE GuildID='"+str(ctx.guild.id)+"'")
      prefix = tools.cursor.fetchall()
      embed = tools.buildembed("Prefix", f"The command prefix for this server is `{prefix[0][0]}`")
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
  
  #Word Filter Settings
  @commands.command(aliases=['wf'])
  async def wordfilter(self, ctx, payload = None, *, word = None):
    if ctx.message.author.guild_permissions.manage_channels:
      if payload != None:
        if payload.lower() == 'remove':
          try:
            tools.cursor.execute("DELETE FROM WordFilter WHERE Word=? AND GuildID=?", (word, ctx.guild.id,))
            tools.db.commit()
          except:
            embed = tools.buildembed("Word Filter", f"{word} could not be found in the words list")
            await ctx.send(embed=embed)
          else:
            embed = tools.buildembed("Word Filter", f"{word} has been successfully removed")
            await ctx.send(embed=embed)
        elif payload.lower() == 'list':
          bword = await tools.read("WordFilter", "Word", ctx.guild.id)
          embed = tools.buildembed("List of Banned Words/Phrases", "Items are inside of spoiler tags")
          for i in bword:
            embed.add_field(name=f"Word", value=f"||{i[0]}||", inline=False)
          await ctx.send(embed=embed)
        elif payload.lower() == 'add':
          bword = await tools.read("WordFilter", "Word", ctx.guild.id)
          bwords = [''.join(i) for i in bword]
          if len(bwords) < 11:
            if not word == None:
              if len(word) < 257:
                tools.cursor.execute("INSERT INTO WordFilter(GuildID, Word) VALUES(?, ?)", (ctx.guild.id, word))
                tools.db.commit()
                embed = tools.buildembed("Word Filter", f"{word} added successfully")
                await ctx.send(embed=embed)
        else:
          embed = tools.buildembed("Word Filter", f"invalid argument. For a list of arguments, use\n `{ctx.prefix}wordfilter`")
          await ctx.send(embed=embed)
      else:
        embed = tools.buildembed("Word Filter", "Info")
        embed.add_field(name="Toggle", value=f"To toggle the word filter on and off, use `{ctx.prefix}wordfilter toggle`", inline=False)
        embed.add_field(name="Add", value=f"To add a word to the filter, use `{ctx.prefix}wordfilter add [word]`\nYou can use a phrase or a word\nWords/phrases must be under 256 characters, and a maximum of 10 words/phrases can be banned", inline=False)
        embed.add_field(name="Remove", value=f"To remove a word from the filter, use `{ctx.prefix}wordfilter remove [word]`", inline=False)
        embed.add_field(name="List", value=f"To view a list of banned words, use `{ctx.prefix}wordfilter list`", inline=False)
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
  @commands.group()
  async def log(self, ctx):
    if ctx.message.author.guild_permissions.manage_channels:
      if ctx.invoked_subcommand == None:
        embed = tools.buildembed("Log Settings", f"To change the channel used for logging, use {ctx.prefix}log [event] [channel]\nTo disable logging of specific events, use {ctx.prefix}log [event]\nHere's a list of events")
        embed.add_field(name="When the clear command is used", value=f"clear")
        embed.add_field(name="When messages are deleted", value=f"deletedmessages")
        embed.add_field(name="When a member is banned from this server", value=f"ban")
        embed.add_field(name="When a member is kicked from this server", value=f"kick")
        embed.add_field(name="When a member is assigned the time out role", value=f"timeout")
        embed.add_field(name="When a member uses a banned word", value="wordf")
        await ctx.send(embed=embed)
  #Changes the log channel
  @log.command(aliases=['delmsg'])
  async def deletedmessages(self, ctx, payload=None):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        await tools.update("Log", "DelMsg", 0, ctx.guild.id)
        tools.db.commit()
      else:
        await tools.update("Log", "DelMsg", payload.id, ctx.guild.id)
        tools.db.commit()
        embed = tools.buildembed("Log", "Event value successfully changed")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  @log.command(aliases=['b'])
  async def ban(self, ctx, payload=None):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        await tools.update("Log", "Ban", 0, ctx.guild.id)
        tools.db.commit()
      else:
        await tools.update("Log", "Ban", payload.id, ctx.guild.id)
        tools.db.commit()
        embed = tools.buildembed("Log", "Event value successfully changed")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  @log.command(aliases=['k'])
  async def kick(self, ctx, payload=None):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        await tools.update("Log", "Kick", 0, ctx.guild.id)
        tools.db.commit()
      else:
        await tools.update("Log", "Kick", payload.id, ctx.guild.id)
        tools.db.commit()
        embed = tools.buildembed("Log", "Event value successfully changed")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  @log.command(aliases=['timedout', 'to'])
  async def timeout(self, ctx, payload=None):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        await tools.update("Log", "Timeout", 0, ctx.guild.id)
        tools.db.commit()
      else:
        await tools.update("Log", "Timeout", payload.id, ctx.guild.id)
        tools.db.commit()
        embed = tools.buildembed("Log", "Event value successfully changed")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  @log.command(aliases=['c', 'purge', 'p'])
  async def clear(self, ctx, payload=None):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        await tools.update("Log", "Clear", 0, ctx.guild.id)
        tools.db.commit()
      else:
        await tools.update("Log", "Clear", payload.id, ctx.guild.id)
        tools.db.commit()
        embed = tools.buildembed("Log", "Event value successfully changed")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
  @log.command(aliases=['wfilter'])
  async def wordf(self, ctx, payload=None):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        payload = await TextChannelConverter().convert(ctx, str(payload))
      except:
        await tools.update("Log", "WordFilter", 0, ctx.guild.id)
        tools.db.commit()
      else:
        await tools.update("Log", "WordFilter", payload.id, ctx.guild.id)
        tools.db.commit()
        embed = tools.buildembed("Log", "Event value successfully changed")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed("Log", "This command requires the manage channels permission")
      await ctx.send(embed=embed)
    
  @commands.command(aliases=['timedoutrole', 'tor'])
  async def timeoutrole(self, ctx, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles == True:
      await tools.update("GuildConfig", "TimeOutRole", role.id, ctx.guild.id)
      tools.db.commit()
      embed = tools.buildembed("Mute Role", description="Successfully changed to "+role.name)
      await ctx.send(embed=embed)
  @timeoutrole.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, commands.RoleNotFound) or isinstance(error, commands.MissingRequiredArgument):
      embed = tools.buildembed(title="Muted Role", description="You did not specify a valid role (name or ID, case sensitive)")
      await ctx.send(embed=embed)
  
  @commands.command(aliases= ['bl', 'cbl', 'commandblocklist'])
  async def blocklist(self, ctx, channel: discord.TextChannel):
    if ctx.author.guild_permissions.manage_channels == True:
      bchannel = await tools.read("CommandBlocklist", "Channel", ctx.guild.id)
      bchannels = [''.join(i) for i in bchannel]
      if channel.id in bchannels:
        tools.cursor.execute("DELETE FROM CommandBlocklist WHERE Channel=?", (channel.id))
        tools.db.commit()
        embed = tools.buildembed("Command Blocklist", f"{channel.mention} was removed from the blocklist")
        await ctx.send(embed=embed)
      else:
         tools.cursor.execute("INSERT INTO CommandBlocklist(GuildID, Channel) VALUES(?, ?)", (ctx.guild.id, channel.id))
         tools.db.commit()
         embed = tools.buildembed("Command Blocklist", f"{channel.mention} was added to the the blocklist")
         await ctx.send(embed=embed)
  @blocklist.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, commands.ChannelNotFound) or isinstance(error, commands.MissingRequiredArgument):
      embed = tools.buildembed("Command Blocklist", "Channel could not be found")
      await ctx.send(embed=embed)





def setup(bot):
  bot.add_cog(Settings(bot))
