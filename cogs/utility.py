import discord
from discord.ext import commands
from discord.ext.commands import bot, MemberConverter, TextChannelConverter, EmojiConverter, PartialEmojiConverter, RoleConverter
import json
import asyncio
import cfg
import sdb
class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  @commands.command()
  async def invite(self, ctx):
    if 'VANITY_URL' in ctx.guild.features:
      invites = await ctx.guild.vanity_invite()
      await ctx.send(invites.url)
    else:
      invites = await ctx.guild.invites()
      await ctx.send(invites[0])
  
  @commands.command(aliases=['se', 'showemoji', 'stealemoji', 'stealemote', 'viewemote', 'viewemoji'])
  async def showemote(self, ctx, emote = None):
    if emote == None:
      embed = cfg.buildembed("Show Emote", "You didn't specify an emote for me to find")
    else:
      try:
        emote = await PartialEmojiConverter().convert(ctx, emote)
      except:
        embed = cfg.buildembed('Show Emote', "I couldn't find the emote you were looking for")
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
  async def membercount(self, ctx, *, role = None):
    try:
      role = await RoleConverter().convert(ctx, role)
    except:
      embed = cfg.buildembed('Member Count', f'There are {len(ctx.guild.members)} in this server')
      await ctx.send(embed=embed)
    else:
      if len(role.members) == 1:
        embed = cfg.buildembed('Member Count', f'There is 1 member with the {role.name} role in {ctx.guild.name}')
        await ctx.send(embed=embed)
      else:
        embed = cfg.buildembed('Member Count', f'There are {len(role.members)} members with the {role.name} role in {ctx.guild.name}')
        await ctx.send(embed=embed)
  
  @commands.command()
  async def poll(self, ctx, channel = None):
    if ctx.author.guild_permissions.manage_messages == True:
      try:
        channel = await TextChannelConverter().convert(ctx, channel)
      except:
        channel = ctx.channel
    else:
      channel = ctx.channel
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    embed = cfg.buildembed('Poll', 'Enter a poll question')
    await ctx.send(embed=embed)
    try:
      desc = await self.bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
      embed = cfg.buildembed('Poll', "I got tired of waiting for you to say something. Try again later, alright?")
      await ctx.send(embed=embed)
    else:
      count = 0
      embed = cfg.buildembed('Poll', 'Enter up to 5 poll options. Say `done` when finished')
      await ctx.send(embed=embed)
      embed = cfg.buildembed('Poll', desc.content)
      while count < 5:
        try:
          option = await self.bot.wait_for('message', timeout=60.0, check=check)
          if option.content.lower() == 'done':
            break
          key = ['\N{REGIONAL INDICATOR SYMBOL LETTER A}', '\N{REGIONAL INDICATOR SYMBOL LETTER B}', '\N{REGIONAL INDICATOR SYMBOL LETTER C}', '\N{REGIONAL INDICATOR SYMBOL LETTER D}', '\N{REGIONAL INDICATOR SYMBOL LETTER E}']
          embed.add_field(name='\u200b', value=f'{key[count]} {option.content}', inline=False)
          await option.delete(delay=1.0)
          count += 1
        except asyncio.TimeoutError:
          embed = cfg.buildembed('Poll', "I got tired of waiting for you to say something\nTry again when you've made up your mind, okay?")
      await channel.send(embed=embed)
      if embed.fields != discord.Embed.Empty:
        message = await channel.fetch_message(channel.last_message_id)
        count = -1
        for i in embed.fields:
          count += 1
          await message.add_reaction(key[count])
  
  @commands.command(aliases=['rc', 'rolecolor', 'editcolor', 'editcolour'])
  async def rolecolour(self, ctx, hx = None, *, role = None):
    try:
      role = await RoleConverter().convert(ctx, role)
      await role.edit(colour = discord.Colour(int(hx, base=16)))
      embed = cfg.buildembed('Role Colour', f'{role.name} was edited successfuly', colour=discord.Colour(int(hex, base=16)))
      await ctx.send(embed=embed)
    except:
      embed = cfg.buildembed('Role Colour', 'Something went wrong, please try again')
      await ctx.send(embed=embed)
  
  @commands.Cog.listener()
  async def on_raw_message_delete(self, deleted_message):
    log = await sdb.read('Log', 'DelMsg', deleted_message.guild_id)
    if len(str(log)) > 1:
      if deleted_message.cached_message == None:
        try:
          log = self.bot.get_channel(log)
        except:
          pass
        else:
          channel = self.bot.get_channel(deleted_message.channel_id)
          embed = cfg.buildembed('Message Deleted', f'in {channel.mention}', discord.Colour.red())
          embed.add_field(name='Message ID', value=deleted_message.message_id)
          embed.add_field(name='Message Content Unavailable', value="The message wasn't cached in time for it to be logged, sorry")
          await log.send(embed=embed)
      else:
        if not deleted_message.cached_message.author.bot:
          try:
            log = self.bot.get_channel(log)
          except:
            pass
          else:
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
    log = await sdb.read('Log', 'Ban', guild.id)
    if len(log) > 1:
      ban = await guild.fetch_ban(user)
      embed = cfg.buildembed("Member banned", f"{str(user)} was banned from {guild}", discord.Colour.red())
      embed.add_field(name="Reason", value=ban.reason)
      channel = self.bot.get_channel(log)
      await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    wel = await sdb.read("GuildConfig", "Welcome", member.guild.id)
    if wel == True:
      channel = await sdb.read("GuildConfig", "WelcomeChannel", member.guild.id)
      channel = self.bot.get_channel(channel)
      key = {'MENTION': member.mention, 'SERVER': member.guild.name}
      msg = await sdb.read("GuildConfig", "WelcomeMessage", member.guild.id)
      await channel.send(msg.format(**key))


  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    tmp = await sdb.read("PBConfig", "Enabled", payload.guild_id)
    if tmp == 1:
      del tmp
      if payload.emoji.name == '\N{PINEAPPLE}':
        channel = sdb.read("PBConfig", "Channel", payload.guild_id)
        channel = self.bot.get_channel(channel)
        rchannel= self.bot.get_channel(payload.channel_id)
        rmessage = await rchannel.fetch_message(payload.message_id)
        for reaction in rmessage.reactions:
          if reaction.emoji == '\N{PINEAPPLE}':
            reaction = reaction
            break
        cnt = sdb.read("PBConfig", "Count", payload.guild_id)
        if reaction.count > cnt:
          def predicate(msg):
            return msg.author.bot
          async for m in channel.history(limit=10).filter(predicate):
            if int(m.embeds[0].fields[0].value[82:].replace(")", "")) == reaction.message.id:
              for r in reaction.message.reactions:
                if r.emoji == '\N{PINEAPPLE}':
                  count = r.count
                break
              embed = m.embeds[0]
              embed.set_footer(text=f'Highest\N{PINEAPPLE}: {count}')
              await m.edit(embed=embed)
              break
        elif reaction.count == cnt:
          if reaction.message.channel != channel: 
            embed = cfg.buildembed(str(reaction.message.author), reaction.message.content, discord.Colour.gold())
            embed.add_field(name="Original Message", value=f"[Jump Link]({reaction.message.jump_url})", inline=False)
            embed.set_thumbnail(url=reaction.message.author.avatar_url)
            embed.set_footer(text=f'Highest {reaction.emoji}: {reaction.count}')
            att = rmessage.attachments
            if len(att) != 0:
              if att[0].url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                  embed.set_image(url=att[0].url)
              else:
                  embed.add_field(name='Message Attachment', value=f'[{att[0].filename}]({att[0].url})', inline=False)
            await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Utility(bot))
