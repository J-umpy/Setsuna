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
            embed = cfg.buildembed(f'List of {event.title()}s', None)
            action = getattr(discord.AuditLogAction,event)
            async for entry in ctx.guild.audit_logs(limit = 15, action=action):
              embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
            await ctx.channel.send(embed=embed)
          except:
            await ctx.channel.send("You either didn't specify an action, or you didn't specify a user. For a list of actions, use .help actionlist")
        else:
          try:
            embed = cfg.buildembed(f'List of actions by {event.title()}', None)
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
          embed = cfg.buildembed(f'Action list for {member}', None)
          action = getattr(discord.AuditLogAction,event)
          async for entry in ctx.guild.audit_logs(limit = 15, action=action, user=member):
            embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
          await ctx.channel.send(embed=embed)
  
  @commands.command(aliases=['banlog'])
  async def banlist(self, ctx, page = None):
    embed = cfg.buildembed('List of Banned Users', None)
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

  @commands.command(aliases=['se', 'showemoji', 'stealemoji', 'stealemote', 'viewemote', 'viewemoji'])
  async def showemote(self, ctx, emote = None):
    if emote == None:
      await ctx.send("You didn't specify an emote to show")
    try:
      emote = await EmojiConverter().convert(ctx, emote)
    except:
      try:
        await PartialEmojiConverter.convert(ctx, emote)
      except:
        cfg.buildembed('Show Emote', "I couldn't find the emote you were looking for")
      else:
        emote = emote.replace('<', '')
        emote = emote.replace('>', '')
        emote = emote.rsplit(':', 2)
        embed = cfg.buildembed(emote[1], f"ID: {emote[2]}")
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{emote[2]}.png")
        await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed(emote.name, f"ID: {emote.id}")
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
    embed = cfg.buildembed(str(member), 'Information', colour)
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
      embed = cfg.buildembed('Member Count', f'There are {len(ctx.guild.members)} in this server')
      await ctx.send(embed=embed)
    else:
      role = len(role.members)
      if role == 1:
        embed = cfg.buildembed('Member Count', f'There is 1 member with the {role.name} role in {ctx.guild.name}')
        await ctx.send(embed=embed)
      else:
        embed = cfg.buildembed('Member Count', f'There are {role} members with the {role.name} role in {ctx.guild.name}')
        await ctx.send(embed=embed)
  
  @commands.Cog.listener()
  async def on_raw_message_delete(self, deleted_message):
    if deleted_message.cached_message == None:
      log = self.bot.get_channel(cfg.data['deletedmessageschannel'])
      channel = self.bot.get_channel(deleted_message.channel_id)
      embed = cfg.buildembed('Message Deleted', f'in {channel.mention}', discord.Colour.red())
      embed.add_field(name='Message ID', value=deleted_message.message_id)
      embed.add_field(name='Message Content Unavailable', value="The message wasn't cached in time for it to be logged, sorry")
      await log.send(embed=embed)
    else:
      if not deleted_message.cached_message.author.bot:
        log = self.bot.get_channel(cfg.data['deletedmessageschannel'])
        channel = self.bot.get_channel(deleted_message.channel_id)
        embed = cfg.buildembed('Message Deleted', f'in {channel.mention}', discord.Colour.red())
        embed.add_field(name='Message ID', value=deleted_message.message_id)
        embed.add_field(name='Message Author', value=deleted_message.cached_message.author)
        embed.add_field(name='Message Author Nickname', value=deleted_message.cached_message.author.display_name)
        embed.add_field(name='Message Author Mention (If Available)', value=deleted_message.cached_message.author.mention)
        embed.add_field(name='Messasge Content', value=deleted_message.cached_message.content, inline=False)
        await log.send(embed=embed)
      
  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):
    ban = await guild.fetch_ban(user)
    embed = cfg.buildembed("Member banned", f"{str(user)} was banned from {guild}", discord.Colour.red())
    embed.add_field(name="Reason", value=ban.reason)
    channel = self.bot.get_channel(cfg.data["logchannel"])
    await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = self.bot.get_channel(cfg.data["welcomechannel"])
    key = {'MENTION': member.mention, 'SERVER': member.guild.name}
    await channel.send(cfg.data["welcome"]["message"].format(**key))

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.emoji.name == '\N{PINEAPPLE}':
      channel = self.bot.get_channel(cfg.data["pineappleboard"]["channel"])
      rchannel= self.bot.get_channel(payload.channel_id)
      rmessage = await rchannel.fetch_message(payload.message_id)
      for reaction in rmessage.reactions:
        if reaction.emoji == '\N{PINEAPPLE}':
          reaction = reaction
          break
      if reaction.count > cfg.data['pineappleboard']['count']:
        async for m in channel.history(limit=5):
          if int(m.embeds[0].fields[0].value[82:].replace(")", "")) == reaction.message.id:
            for r in reaction.message.reactions:
              if r.emoji == '\N{PINEAPPLE}':
                count = r.count
              break
            embed = m.embeds[0]
            embed.set_footer(text=f'Highest {reaction.emoji}: {count}')
            await m.edit(embed=embed)
            break
      elif reaction.count == cfg.data['pineappleboard']['count']:
        if reaction.message.channel != channel: 
          cfg.buildembed(str(reaction.message.author), reaction.message.content, discord.Colour.gold())
          embed.add_field(name="Original Message", value=f"[Jump Link]({reaction.message.jump_url})", inline=False)
          embed.set_thumbnail(url=reaction.message.author.avatar_url)
          embed.set_footer(text=f'Highest {reaction.emoji}: {reaction.count}')
          att = rmessage.attachments[0]
          if att.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
            embed.set_image(url=att.url)
          else:
            embed.add_field(name='Message Attachment', value=f'[{att.filename}]({att.url})', inline=False)
          await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Utility(bot))