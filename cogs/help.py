import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import json
with open('config.json') as f:
  data = json.loads(f.read())

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  
  
  @commands.command(aliases=['help'])
  async def h(self, ctx, payload = None):
    if payload == None: 
      embed = discord.Embed(title = "Welcome to the Help Center!", description = "List of Modules", colour = discord.Colour.blue())
      embed.set_footer(text="Bot by Jumpy♡#0150")
      embed.add_field(name="Administration", value="A list of administrative commands")
      embed.add_field(name="Utility", value="A list of utility commands")
      embed.add_field(name="For more info", value=f"Use {data['prefix']}help [modulename] to see the list of commands")
    else:
      payload = payload.lower()
#Administration
      if payload == 'administration':
        embed = discord.Embed(title = "List of Administrative Commands", description = f"For more info, use {data['prefix']}help [command name]", colour = discord.Colour.blue())
        embed.add_field(name='Ban', value='bans the user from the server', inline=False)
        embed.add_field(name='Kick', value='kicks the user from the server', inline=False)
        embed.add_field(name='Clear', value='deletes a set number of messages', inline=False)
      elif payload == 'ban':
        embed = discord.Embed(title = 'Ban', description = "bans the user from the server", colour = discord.Colour.blue())
        embed.add_field(name='Usage', value=f"{data['prefix']}ban [user to ban] [ban reason (required)]", inline=False)
        embed.add_field(name='Aliases', value='b', inline=False)
      elif payload == 'kick':
        embed = discord.Embed(title = "Kick", description = "kicks the user from the server", colour = discord.Colour.blue())
        embed.add_field(name="Usage", value=f"{data['prefix']}kick [user to kick] [kick reason (required)]", inline=False)
        embed.add_field(name="Aliases", value="k", inline=False)
      elif payload == "clear":
        embed = discord.Embed(title = "Clear", description = "deletes a set number of messages", colour = discord.Colour.blue())
        embed.add_field(name="Usage", value=f"{data['prefix']}clear [number of messages] [user to target (optional)]", inline=False)
        embed.add_field(name="Aliases", value="purge", inline=False)
#Utility
      elif payload.lower() == "utility":
        embed = discord.Embed(title = "List of Utility Commands", description = f"For more info, use {data['prefix']}help [command name]", colour = discord.Colour.blue())
        embed.add_field(name='Mention', value='pings a certain role', inline=False)
        embed.add_field(name='Invite', value='sends the oldest invite', inline=False)
        embed.add_field(name='Banlist', value='sends a paginated list of banned users')
        embed.add_field(name='Actionlist', value='lists audit log actions, accepts tons of parameters', inline=False)
      elif payload == 'mention':
        embed = discord.Embed(title = 'Mention', description = "pings a specified role in the channel the command was sent in", colour = discord.Colour.blue())
        embed.add_field(name='Usage', value=f"{data['prefix']}mention [role]", inline=False)
        embed.add_field(name='Aliases', value='None', inline=False)
      elif payload == 'invite':
        embed = discord.Embed(title = 'Invite', description = "sends the oldest server invite", colour = discord.Colour.blue())
        embed.add_field(name='Usage', value=f"{data['prefix']}invite", inline=False)
        embed.add_field(name='Aliases', value='None', inline=False)
      elif payload == 'banlist':
        embed = discord.Embed(title = 'Banlist', description = "sends a list of banned users", colour = discord.Colour.blue())
        embed.add_field(name='Usage', value=f"{data['prefix']}banlist [page number (optional)]", inline=False)
        embed.add_field(name='Aliases', value='None', inline=False)
      elif payload == 'actionlist':
        embed = discord.Embed(title = 'Action List', description = "lists audit log actions", colour = discord.Colour.blue())
        embed.add_field(name='Usage', value=f"{data['prefix']}actionlist [audit log action (optional)] [user (optional)]", inline=False)
        embed.add_field(name='More Info', value=f"""All fields are optional. 
        Leaving all fields empty will send the most recent actions. 
        The fields can be sent in any order. 
        The "audit log action" field must be sent in Discord's internal format. 
        Example: "{data['prefix']}actionlist Member_Role_Update" would send a list of the most recent role updates""", inline=False)
        embed.add_field(name='Aliases', value="None", inline=False)
    await ctx.send(embed=embed)




def setup(bot):
  bot.add_cog(Help(bot))