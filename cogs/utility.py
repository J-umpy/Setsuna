import discord
from discord.ext import commands
from discord.ext.commands import bot, MemberConverter, TextChannelConverter, EmojiConverter, PartialEmojiConverter, RoleConverter
import json
import asyncio
import tools
class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None
  
  #Sends the most recent invite on a server, or the vanity URL if the server has one
  @commands.command()
  async def invite(self, ctx):
    if 'VANITY_URL' in ctx.guild.features:
      await ctx.send(ctx.guild.vanity_invite())
    else:
      invites = await ctx.guild.invites()
      await ctx.send(invites[0])
  
  # Lists audit log actions, this command is now obsolete due to the mobile audit log overhaul from March 2020's Android Alpha
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
            embed = tools.buildembed(f'List of {event.title()}s', None)
            action = getattr(discord.AuditLogAction,event)
            async for entry in ctx.guild.audit_logs(limit = 15, action=action):
              embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
            await ctx.channel.send(embed=embed)
          except:
            await ctx.channel.send("You either didn't specify an action, or you didn't specify a user. For a list of actions, use .help actionlist")
        else:
          try:
            embed = tools.buildembed(f'List of actions by {event.title()}', None)
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
          embed = tools.buildembed(f'Action list for {member}', None)
          action = getattr(discord.AuditLogAction,event)
          async for entry in ctx.guild.audit_logs(limit = 15, action=action, user=member):
            embed.add_field(name = '{0.user}'.format(entry), value = f'{event.title()}'+' to {0.target} Entry ID: {0.id}'.format(entry), inline = True)
          await ctx.channel.send(embed=embed)
  
  #Lists all banned users
  @commands.command(aliases=['banlog'])
  async def banlist(self, ctx, page = None):
    embed = tools.buildembed('List of Banned Users', None)
    #Calculates the number of pages
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

 # Sends the specified emoji in an embed
  @commands.command(aliases=['se', 'showemoji', 'stealemoji', 'stealemote', 'viewemote', 'viewemoji'])
  async def showemote(self, ctx, emote = None):
    if emote == None:
      await ctx.send("You didn't specify an emote to show")
    try:
      emote = await EmojiConverter().convert(ctx, emote)
    except:
      try:
        await PartialEmojiConverter().convert(ctx, emote)
      except:
        tools.buildembed('Show Emote', "I couldn't find the emote you were looking for")
      else:
        # Filters out the unnecessary characters from the converter's return
        emote = emote.replace('<', '')
        emote = emote.replace('>', '')
        emote = emote.rsplit(':', 2)
        embed = tools.buildembed(emote[1], f"ID: {emote[2]}")
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{emote[2]}.png")
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed(emote.name, f"ID: {emote.id}")
      embed.set_image(url=emote.url)
      await ctx.send(embed=embed)
  
  # Displays a bit of info about the specified user
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
    # Sets the embed colour based on the online status of the specified user
    embed = tools.buildembed(str(member), 'Information', colour)
    embed.add_field(name='Nickname', value=member.display_name, inline=False)
    embed.add_field(name="Highest Role", value=member.top_role, inline=False)
    embed.add_field(name="Joined", value=member.joined_at, inline=False)
    if member.premium_since != None:
      embed.add_field(name="Boosted On", value=member.premium_since, inline=False)
    else:
      embed.add_field(name="Boost Status", value="Not boosting")
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
  
  #Displays the number of members in the server of a given role
  @commands.command()
  async def membercount(self, ctx, role = None):
    try:
      role = await RoleConverter().convert(ctx, role)
    except:
      embed = tools.buildembed('Member Count', f'There are {len(ctx.guild.members)} in this server')
      await ctx.send(embed=embed)
    else:
      rolecount = len(role.members)
      if rolecount == 1:
        embed = tools.buildembed('Member Count', f'There is 1 member with the {role.name} role in {ctx.guild.name}')
        await ctx.send(embed=embed)
      else:
        embed = tools.buildembed('Member Count', f'There are {rolecount} members with the {role.name} role in {ctx.guild.name}')
        await ctx.send(embed=embed)
  
  # Sends the specified user's avatar in an embed
  @commands.command(aliases=['avi'])
  async def avatar(self, ctx, member: discord.Member):
    embed = tools.buildembed(title=member.display_name, description="Avatar")
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)
  #If no user is specified, the sender's avatar is sent instead
  @avatar.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.MissingRequiredArgument):
      embed = tools.buildembed(title=ctx.author.display_name, description="Avatar")
      embed.set_image(url=ctx.author.avatar_url)
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
    # If both values return True, this check is passed and the message that triggered the check is saved to the "desc" variable
    def check(desc):
      return desc.channel == ctx.channel and desc.author == ctx.author
    embed = tools.buildembed('Poll', 'Enter a poll question')
    await ctx.send(embed=embed)
    try:
      #This variable NEEDS to be named the same as the one in the check
      desc = await self.bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
      embed = tools.buildembed('Poll', "I got tired of waiting for you to say something. Try again later, alright?")
      await ctx.send(embed=embed)
    else:
      def check(option):
        return option.channel == ctx.channel and option.author == ctx.author
      count = 0
      embed = tools.buildembed('Poll', 'Enter up to 5 poll options. Say `done` when finished, or `cancel` to cancel')
      await ctx.send(embed=embed)
      embed = tools.buildembed('Poll', desc.content)
      while count < 5:
        try:
          option = await self.bot.wait_for('message', timeout=60.0, check=check)
          if option.content.lower() == 'done':
            break
          elif option.content.lower() == 'cancel':
            embed = tools.buildembed('Poll', 'The poll was cancelled')
            break
          key = ['\N{REGIONAL INDICATOR SYMBOL LETTER A}', '\N{REGIONAL INDICATOR SYMBOL LETTER B}', '\N{REGIONAL INDICATOR SYMBOL LETTER C}', '\N{REGIONAL INDICATOR SYMBOL LETTER D}', '\N{REGIONAL INDICATOR SYMBOL LETTER E}']
          embed.add_field(name='\u200b', value=f'{key[count]} {option.content}', inline=False)
          await option.delete(delay=1.0)
          count += 1
        except asyncio.TimeoutError:
          embed = tools.buildembed('Poll', "I got tired of waiting for you to say something\nTry again when you've made up your mind, okay?")
          break
      await channel.send(embed=embed)
      if embed.fields != discord.Embed.Empty:
        message = await channel.fetch_message(channel.last_message_id)
        count = -1
        for i in embed.fields:
          count += 1
          await message.add_reaction(key[count])
  
  @commands.Cog.listener()
  async def on_message_delete(self, deleted_message):
    if not deleted_message.author.bot:
      log = await tools.read('Log', 'DelMsg', deleted_message.guild.id)
      log = log[0][0]
      if log != 0:
        log = self.bot.get_channel(log)
        channel = self.bot.get_channel(deleted_message.channel.id)
        embed = tools.buildembed('Message Deleted', f'in {channel.mention}', discord.Colour.red())
        embed.add_field(name='Message ID', value=deleted_message.id)
        embed.add_field(name='Message Author', value=deleted_message.author, inline=False)
        embed.add_field(name='Author Nickname', value=deleted_message.author.display_name)
        embed.add_field(name='Author Mention', value=deleted_message.author.mention)
        embed.add_field(name='Messasge Content', value=deleted_message.content, inline=False)
        await log.send(embed=embed)
      
  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):
    channel = await tools.read('Log', 'Ban', guild.id)
    channel = channel[0][0]
    if channel != 0:
      ban = await guild.fetch_ban(user)
      embed = tools.buildembed("Member banned", f"{str(user)} was banned from {guild}", discord.Colour.red())
      embed.add_field(name="Reason", value=ban.reason)
      channel = self.bot.get_channel(channel)
      await channel.send(embed=embed)
  @commands.Cog.listener()
  async def on_member_kick(self, guild, user):
    channel = await tools.read('Log', 'Kick', guild.id)
    channel = channel[0][0]
    if channel != 0:
      embed = tools.buildembed("Member kicked", f"{str(user)} was kicked from {guild}", discord.Colour.red())
      channel = self.bot.get_channel(channel)
      await channel.send(embed=embed)
  
  # Welcome command, disabled temporarily
  # @commands.Cog.listener()
  # async def on_member_join(self, member):
  #   channel = self.bot.get_channel(tools.data["welcomechannel"])
  #   key = {'MENTION': member.mention, 'SERVER': member.guild.name}
  #   await channel.send(tools.data["welcome"]["message"].format(**key))

def setup(bot):
  bot.add_cog(Utility(bot))
