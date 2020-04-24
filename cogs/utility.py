import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import json
with open('config.json') as f:
  data = json.loads(f.read())

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
  async def invite(self, ctx):
    if 'VANITY_URL' in ctx.guild.features:
      await ctx.send(ctx.guild.vanity_invite())
    else:
      invites = await ctx.guild.invites()
      await ctx.send(invites[0])

  @commands.command()
  async def actionlist(self, ctx, event, member = None):
    if ctx.message.author.guild_permissions.manage_messages == False: 
      await ctx.channel.send("You don't have permission to use this command)")
    else:
      if member == None:
        try:
          member = await MemberConverter().convert(ctx, event)
        except:
          try:
            embed = discord.Embed(title = f'List of {event.title()}s', description = None, colour=discord.Colour.blue())
            action = getattr(discord.AuditLogAction,event)
            async for entry in ctx.guild.audit_logs(limit = 15, action=action):
              embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
            await ctx.channel.send(embed=embed)
          except:
            await ctx.channel.send("You either didn't specify an action, or you didn't specify a user. For a list of actions, use .help actionlist")
        else:
          try:
            embed = discord.Embed(title = f'List of actions by {event.title()}', description = None, colour=discord.Colour.blue())
            async for entry in ctx.guild.audit_logs(limit = 15, user=member):
              embed.add_field(name = '{0.user}'.format(entry), value = '{0.action} to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
            await ctx.channel.send(embed=embed)
          except:
            await ctx.channel.send("No user was found by that name")
      else:
        try:
          member = await MemberConverter().convert(ctx, member)
        except:
          await ctx.channel.send("I couldn't find the user you were looking for")
        else:
          embed = discord.Embed(title = f'Action list for {member}', description = None, colour=discord.Colour.blue())
          action = getattr(discord.AuditLogAction,event)
          async for entry in ctx.guild.audit_logs(limit = 15, action=action, user=member):
            embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
          await ctx.channel.send(embed=embed)
  
  @commands.command()
  async def banlist(self, ctx, page = None):
    embed = discord.Embed(title='List of Banned Users', description=None)
    try: 
      page = abs(int(page))
      floor = (page*10) - 10
    except:
      page = 1
      floor = 0
    if floor < 0:
      floor = 0
    bans =  await ctx.guild.bans()
    counter = 0
    while counter < 10:
        embed.add_field(name=bans[floor].user, value=bans[floor].reason, inline=False)
        counter += 1
        floor += 1
    embed.set_footer(text=f'Page {page} of {len(bans)//10}')
    await ctx.send(embed=embed)
    
  
  @commands.Cog.listener()
  async def on_raw_message_delete(self, deleted_message):
    if deleted_message.cached_message == None:
      log = self.bot.get_channel(data['deletedmessageschannel'])
      channel = self.bot.get_channel(deleted_message.channel_id)
      embed = discord.Embed(title = 'Message Deleted', description = f'in {channel.mention}', colour=discord.Colour.red())
      embed.add_field(name='Message ID', value=deleted_message.message_id)
      embed.add_field(name='Message Content Unavailable', value="The message wasn't cached in time for it to be logged, sorry")
      await log.send(embed=embed)
    else:
      if not deleted_message.cached_message.author.bot:
        log = self.bot.get_channel(data['deletedmessageschannel'])
        channel = self.bot.get_channel(deleted_message.channel_id)
        embed = discord.Embed(title = 'Message Deleted', description = f'in {channel.mention}', colour=discord.Colour.red())
        embed.add_field(name='Message ID', value=deleted_message.message_id)
        embed.add_field(name='Message Author', value=deleted_message.cached_message.author.mention)
        embed.add_field(name='Messasge Content', value=deleted_message.cached_message.content, inline=True)
        await log.send(embed=embed)
      
  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):
    ban = await guild.fetch_ban(user)
    embed = discord.Embed(title="Member banned", description=f"{user.mention} was banned from {guild}")
    embed.add_field(name="Reason", value=ban.reason)
    channel = self.bot.get_channel(data["logchannel"])
    await channel.send(embed=embed)

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