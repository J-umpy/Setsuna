import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import json
import tools
#Reads the command descriptions stored on file
with open('helpdesc.json') as f:
  data = json.loads(f.read())

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  
  async def buildhelp(self, ctx, payload, page = 0):
    #Checks if the argument passed is a command
    if commands.Bot.get_command(self.bot, payload) == None:
      #Checks if the argument passed is a cog and lists all cogs if it isn't
      if self.bot.get_cog(payload.title()) == None:
        embed = tools.buildembed("Welcome to the Help Center!", "Here is a list of modules!")
        embed.add_field(name="For more info use", value=f"{ctx.prefix}help [module name]")
        embed.set_footer(text="Bot by Jumpy♡#0150")
        #Removes the errorhandler cog from the list
        coglist = await tools.fetch_cogs()
        coglist.remove('errorhandler')
        for cog in coglist:
          embed.add_field(name=cog.title(), value=f"A list of commands in the {cog.title()} Module", inline=False)
      #Lists all commands in a cog inside of an embed
      else:
        cog = self.bot.get_cog(payload.title())
        embed = tools.buildembed(f"List of {payload.title()} Commands", f"For more information use {ctx.prefix}help [command name]")
        count = 0
        try:
          int(page)
          floor = (page*10) - 10
        except:
          page = 1
          floor = 0
        if page < 1:
          page = 1
        commandlist = cog.get_commands()
        total = len(commandlist)
        if total < 10:
          total = 10
        commandlist = commandlist[floor:]
        for cmd in commandlist:
          if count < 10:
            try:
              embed.add_field(name=cmd.name, value=data[payload.lower()][cmd.name]['description'], inline=False)
            except:
              pass
            count += 1
          else:
            break
        embed.set_footer(text=f"Page {page} of {total//10}")
    #Grabs detailed info on a specific command from helpdesc.json
    else:
      try:
        command = commands.Bot.get_command(self.bot, payload)
        embed = tools.buildembed(command.name.title(), data[command.cog.qualified_name.lower()][command.name]['description'])
        embed.add_field(name='Usage', value=f"{ctx.prefix}{data[command.cog.qualified_name.lower()][command.name]['usage']}", inline=False)
        embed.add_field(name='Info', value=data[command.cog.qualified_name.lower()][command.name]['info'], inline=False)
        if len(command.aliases) > 0:
          if len(command.aliases) > 1:
            aliaslist = ''
            for alias in command.aliases:
              aliaslist += f"{alias}, "
          else:
            aliaslist = command.aliases[0]
        else:
          aliaslist = 'None'
        embed.add_field(name='Aliases', value=aliaslist, inline=False)
      except:
        embed = tools.buildembed('Error', 'An error has occured. Malformed or missing command description.')
    return embed
  
  @commands.command(aliases=['h'])
  async def help(self, ctx, payload = 'None', page = 0):
    embed = await Help.buildhelp(self, ctx, payload, page)
    await ctx.send(embed=embed)
def setup(bot):
  bot.add_cog(Help(bot))