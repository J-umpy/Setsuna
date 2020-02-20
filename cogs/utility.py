import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import json
with open('config.json') as f:
  data = json.loads(f.read())
bot = commands.Bot(command_prefix=data["prefix"])

class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  @commands.command()
  async def mention(self, ctx):
    role = ctx.message.content[len(data["prefix"]) + len(ctx.invoked_with) + 1:]
    try:
      role = get(ctx.guild.roles, name = role)
    except:
      await ctx.channel.send("Role not found")
    else:
      try:
        await role.edit(mentionable = True, reason = f"Called on by: {ctx.message.author}")
        await ctx.channel.send(role.mention)
        await role.edit(mentionable = False, reason = f"Called on by: {ctx.message.author}")
      except:
        await ctx.channel.send("Missing Permissions")
  @commands.command()
  async def actionlist(self, ctx, event, member = None):
    if ctx.message.author.guild_permissions.manage_messages == False: 
      await ctx.channel.send("You don't have permission to use this command)")
    else:
      if member == None:
        embed = discord.Embed(title = f'List of {event.title()}s', description = None, colour=discord.Colour.blue())
        action = getattr(discord.AuditLogAction,event)
        async for entry in ctx.guild.audit_logs(limit = 15, action=action):
          embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
        await ctx.channel.send(embed=embed)
      else:
        try:
          member = await MemberConverter().convert(ctx, member)
        except:
          print("\nError in command: Ban:\nUser not found, or no user was specified")
        embed = discord.Embed(title = f'Action list for {member.mention}', description = None, colour=discord.Colour.blue())
        action = getattr(discord.AuditLogAction,event)
        async for entry in ctx.guild.audit_logs(limit = 15, action=action, user=member):
          embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
        await ctx.channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    general = self.bot.get_channel(int(data["generalchannel"]))
    if general is None:
      print("the command didn't work LOL YOU SUCK")
    welcomemessage = f"Welcome, {member.mention}! Come join us in {general.mention}"
    embed = discord.Embed(title = "Welcome", description = welcomemessage, colour=discord.Colour.blue())
    embed.set_footer(text="We're glad to have you")
    embed.set_image(url=data["welcomeimage"])
    channel = self.bot.get_channel(int(data["welcomechannel"]))
    await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Utility(bot))
