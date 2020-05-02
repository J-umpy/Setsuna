import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import json
import cfg
with open('cmddesc.json') as f:
  data = json.loads(f.read())
class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  @commands.command(aliases=['h'])
  async def help(self, ctx, payload = "ersjioghsouighouis"):
    async def buildhelp(ctx, payload):
      if commands.Bot.get_command(self.bot, payload) == None:
        if self.bot.get_cog(payload.title()) == None:
          embed = cfg.buildembed("Welcome to the Help Center!", "Here is a list of modules")
          embed.add_field(name="For more info use", value=f"{ctx.prefix}help [module name]")
          embed.set_footer(text="Bot by Jumpy♡#0150")
          for cog in cfg.cogs:
            embed.add_field(name=cog.replace('cogs.', '').title(), value=f"A list of commands in the {cog.replace('cogs.', '').title()} Module", inline=False)
        else:
          cog = self.bot.get_cog(payload.title())
          embed = cfg.buildembed(f"List of {payload.title()} Commands", f"For more information use {ctx.prefix}help [command name]")
          for cmd in cog.get_commands():
            embed.add_field(name=cmd.name, value=data[payload.lower()][cmd.name]['description'], inline=False)
      else:
        command = commands.Bot.get_command(self.bot, payload)
        embed = cfg.buildembed(command.name.title(), data[command.cog.qualified_name.lower()][command.name]['description'])
        embed.add_field(name='Usage', value=f"{ctx.prefix}{data[command.cog.qualified_name.lower()][command.name]['usage']}", inline=False)
        embed.add_field(name='Info', value=data[command.cog.qualified_name.lower()][command.name]['info'], inline=False)
        if len(command.aliases) > 1:
          aliaslist = ""
          for alias in command.aliases:
            aliaslist += f"{alias}, "
        else:
          aliaslist = command.aliases[0]
        embed.add_field(name='Aliases', value=aliaslist, inline=False)
      return embed
    embed = await buildhelp(ctx, payload)
    await ctx.send(embed=embed)
def setup(bot):
  bot.add_cog(Help(bot))