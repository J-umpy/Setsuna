import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import EmojiConverter
from discord.ext.commands import RoleConverter
import json
import asyncio
import cfg
class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

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
  
  @commands.command(aliases=['banlog'])
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
      log = self.bot.get_channel(cfg.data['deletedmessageschannel'])
      channel = self.bot.get_channel(deleted_message.channel_id)
      embed = discord.Embed(title = 'Message Deleted', description = f'in {channel.mention}', colour=discord.Colour.red())
      embed.add_field(name='Message ID', value=deleted_message.message_id)
      embed.add_field(name='Message Content Unavailable', value="The message wasn't cached in time for it to be logged, sorry")
      await log.send(embed=embed)
    else:
      if not deleted_message.cached_message.author.bot:
        log = self.bot.get_channel(cfg.data['deletedmessageschannel'])
        channel = self.bot.get_channel(deleted_message.channel_id)
        embed = discord.Embed(title = 'Message Deleted', description = f'in {channel.mention}', colour=discord.Colour.red())
        embed.add_field(name='Message ID', value=deleted_message.message_id)
        embed.add_field(name='Message Author', value=deleted_message.cached_message.author)
        embed.add_field(name='Message Author Nickname', value=deleted_message.cached_message.author.display_name)
        embed.add_field(name='Message Author Mention (If Available)', value=deleted_message.cached_message.author.mention)
        embed.add_field(name='Messasge Content', value=deleted_message.cached_message.content, inline=False)
        await log.send(embed=embed)
      
  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):
    ban = await guild.fetch_ban(user)
    embed = discord.Embed(title="Member banned", description=f"{str(user)} was banned from {guild}")
    embed.add_field(name="Reason", value=ban.reason)
    channel = self.bot.get_channel(cfg.data["logchannel"])
    await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = self.bot.get_channel(cfg.data["welcomechannel"])
    key = {'MENTION': 'member.mention'}
    await channel.send(cfg.data["welcome"]["message"].format(**key))

  @commands.command(aliases=['se', 'showemoji', 'stealemoji', 'stealemote'])
  async def showemote(self, ctx, emote = None):
    if emote == None:
      await ctx.send("You didn't specify an emote to show")
    try:
      emote = await EmojiConverter().convert(ctx, emote)
    except:
      if not '>' in emote:
        await ctx.send("Invalid Emote")
      else:
        emote = emote.replace('<', '')
        emote = emote.replace('>', '')
        emote = emote.rsplit(':', 2)
        embed = discord.Embed(title=emote[1], description=f"ID: {emote[2]}")
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{emote[2]}.png")
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title=emote.name, description=f"ID: {emote.id}")
      embed.set_image(url=emote.url)
      await ctx.send(embed=embed)
  
  @commands.command(aliases=['ui', 'userinformation', 'whois'])
  async def userinfo(self, ctx, member = None):
    try:
      member = await MemberConverter().convert(ctx, member)
    except:
      member = ctx.message.author
    if member.status == discord.Status.online:
      colour = discord.Colour.green()
    elif member.status == discord.Status.offline:
      colour = discord.Colour.light_grey()
    elif member.status == discord.Status.idle:
      colour = discord.Colour.gold()
    elif member.status == discord.Status.dnd:
      colour = discord.Colour.red()
    embed = discord.Embed(title=str(member), description='Information', colour=colour)
    embed.add_field(name='Nickname', value=member.display_name, inline=False)
    embed.add_field(name="Highest Role", value=member.top_role, inline=False)
    embed.add_field(name="Joined", value=member.joined_at, inline=False)
    if member.premium_since != None:
      embed.add_field(name="Boosted On", value=member.premium_since, inline=False)
    else:
      embed.add_field(name="Boost Status", value="Not boosting")
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
  
  @commands.command()
  async def membercount(self, ctx, role = None):
    try:
      role = await RoleConverter().convert(ctx, role)
    except:
      await ctx.send(f"There are {len(ctx.guild.members)} members in this server")
    else:
      if len(role.members) == 1:
        await ctx.send(f"There is {len(role.members)} member with the {role.name} role")
      else:
        await ctx.send(f"There are {len(role.members)} members with the {role.name} role")

        

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if reaction.emoji == '\N{PINEAPPLE}':
      if reaction.count == cfg.data["pbcount"]:
        channel = self.bot.get_channel(cfg.data["pineappleboard"])
        if reaction.message.channel != channel: 
          embed = discord.Embed(title=str(reaction.message.author), description=reaction.message.content, colour=discord.Colour.gold())
          embed.add_field(name=reaction.message.channel.mention, value=f"[Jump Link]({reaction.message.jump_url})")
          embed.set_thumbnail(url=reaction.message.author.avatar_url)
          await asyncio.sleep(30)
          count = await reaction.message.channel.fetch_message(reaction.message.id)
          count = count.reactions
          leng = len(reaction.message.reactions)-1
          embed.set_footer(text=f'{count[leng].count} {reaction.emoji}')
          if reaction.message.attachments != None:
            embed.set_image(url=reaction.message.attachments[0].url)
          await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Utility(bot))