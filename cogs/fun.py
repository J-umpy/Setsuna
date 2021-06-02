import discord
from discord.ext import commands
from discord.ext.commands import bot, TextChannelConverter
import random
import json
import asyncio
import tools
import urllib
class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  # Quick addition bonus game for the counting game
  async def qmath(self, ctx, loop, num, rannum):
    rannum = rannum + num
    def chck(m):
      return m.channel == ctx.channel and m.author.bot != True
    try:
      msg = await self.bot.wait_for('message', timeout=5.0, check=chck)
    except asyncio.TimeoutError:
      embed = tools.buildembed('Mini Bonus!', "Timed out, let's go back to the main game!")
    try:
      msg = int(msg.content)
    except:
      embed = tools.buildembed('Mini Bonus!', "That's not even a number, back to the main game!", discord.Colour.red())
    if msg == rannum:
      loop += 5
      embed = tools.buildembed('Mini Bonus!', f'You win!\nYour score is now {loop}\nLast recorded number: {num-1}', discord.Colour.green())
    else:
      embed = tools.buildembed('Mini Bonus!', f"You lose! \nThe answer was {rannum}\nYour score is {loop}, now let's get back to it\nLast recorded number: {num-1}", discord.Colour.red())
    await ctx.send(embed=embed)
    return loop, num
  # Number guessing bonus game for the counting game
  async def numberguessing(self, ctx, loop, embed, num):
    ans = random.randint(1, 100)
    tries = 5
    def chck(m):
      return m.channel == ctx.channel and m.author.bot != True
    while tries != 0:
      await ctx.send(embed=embed)
      try:
        msg = await self.bot.wait_for('message', timeout=10.0, check=chck)
      except asyncio.TimeoutError:
        embed = tools.buildembed('Bonus Time!', "Timed Out, let's go back to the main game!")
      try:
        msg = int(msg.content)
      except:
        tries = tries - 1
        embed = tools.buildembed('Bonus Time!', f'Your guess was invalid. {tries} tries remaining')
        continue
      else:
        if msg > ans:
          tries = tries - 1
          embed = tools.buildembed('Bonus Time!', f'The number is lower\n {tries} tries remaining')
        elif msg < ans:
          tries = tries - 1
          embed = tools.buildembed('Bonus Time!', f'The number is higher\n {tries} tries remaining')
        else:
          loop = loop + loop
          embed = tools.buildembed('Bonus Time!', f'You win!\nYour score is now {loop}\nLast recorded number: {num-1}', discord.Colour.green())
          await ctx.send(embed=embed)
          break
    if tries == 0:
      embed = tools.buildembed('Bonus Game!', f'You lost!\nThe number was {ans}.\nYour score is {loop}, now back to The Counting Game! Last recorded number: {num-1}', discord.Colour.red())
      await ctx.send(embed=embed)
    return loop, num
  
  #Counting game
  @commands.group(aliases=['countinggame', 'counting'])
  async def count(self, ctx):
    if ctx.invoked_subcommand == None:
      bchannels = await tools.read("CountBlocklist", "Channel", ctx.guild.id)
      if not ctx.channel.id in bchannels or ctx.message.author.guild_permissions.manage_messages == True:
        num = random.randint(1, 1000)
        await ctx.send(f'The Counting Game has begun! Start counting up!\n{num-1}')
        def check(m):
          return m.channel == ctx.channel
        loop = 0
        while True:
          num = str(num)
          try:
            message = await self.bot.wait_for('message', timeout=10.0, check=check)
          except asyncio.TimeoutError:
            embed = tools.buildembed('Counting Game', f'No one sent a message for 10 seconds, so the game ended. Your score was {loop}')
            await ctx.send(embed=embed)
            break
          else:
            if message.content != num:
              embed = tools.buildembed('Counting Game', f'Game Over! Your score is {loop}')
              await ctx.send(embed=embed)
              break
            else:
              loop += 1
              num = int(num)
              num += 1
              # Rolls for bonus games, 4% chance on every count for the number guessing game, and 7% chance for a quick math problem
              if random.randint(1, 25) == 10:
                #embed = tools.buildembed('Bonus Time!', f'If you successfully complete the bonus challenge, your score of {loop} will be doubled!')
                #await ctx.send(embed=embed) -- IGNORE
                embed = tools.buildembed('Bonus Time!', "Guess what number I am thinking of! It's between 1 and 100, inclusive")
                loop, num = await Fun.numberguessing(self, ctx, loop, embed, num)
              elif random.randint(1, 100) < 8:
                rannum = random.randint(-100, 100)
                if rannum < 0:
                  embed = tools.buildembed('Mini Bonus!', f"Quickly subtract {abs(rannum)} from {num-1}!")
                else:
                  embed = tools.buildembed('Mini Bonus!', f"Quickly add {rannum} to {num-1}!")
                await ctx.send(embed=embed)
                loop, num = await Fun.qmath(self, ctx, loop, num-1, rannum)

  #Count blocklist
  @count.command(aliases=['bl'])
  async def blocklist(self, ctx, channel: discord.TextChannel):
    if ctx.author.guild_permissions.manage_channels == True:
      bchannels = await tools.read("CountBlocklist", "Channel", ctx.guild.id)
      if channel.id in bchannels:
        tools.cursor.execute("DELETE FROM CountBlocklist WHERE Channel=?", (channel.id))
        tools.db.commit()
        embed = tools.buildembed('Count Blocklist', f'Successfully unblocklisted {channel.mention}')
        await ctx.send(embed=embed)
      else: 
        tools.cursor.execute("INSERT INTO CountBlocklist(GuildID, Channel) VALUES(?, ?)", (ctx.guild.id, channel.id))
        tools.db.commit()
        embed = tools.buildembed('Count Blocklist', f'{channel.mention} has been successfully blocklisted')
        await ctx.send(embed=embed)
    else:
      embed = tools.buildembed('Count Blocklist', 'This command requires the manage channels permission')
      await ctx.send(embed=embed)  
  @blocklist.error
  async def sendcmd_handler(self, ctx, error):
    if isinstance(error, commands.ChannelNotFound) or isinstance(error, commands.MissingRequiredArgument):
      embed = tools.buildembed('Count Blocklist', 'Channel could not be found')
      await ctx.channel.send(embed=embed)
    
  @commands.command()
  async def say(self, ctx, *, message = None):
    if ctx.author.guild_permissions.manage_messages == True:
      if message != None or len(ctx.message.attachments) != 0:
        embed = tools.buildembed(self.bot.user.name, message)
        if len(ctx.message.attachments) > 0:
          embed.set_image(url=ctx.message.attachments[0].url)
        await ctx.message.delete(delay=0.5)
        await ctx.send(embed=embed)

  @commands.command()
  async def inspire(self, ctx):
    request = urllib.request.Request("https://inspirobot.me/api?generate=true", None,{'User-Agent':"Setsuna"})
    embed = tools.buildembed("Feel Inspired", "")
    request =str(urllib.request.urlopen(request).read().decode('UTF-8'))
    embed.set_image(url=request)
    embed.set_footer(text="Brought to you by Inspirobot")
    await ctx.send(embed = embed)


def setup(bot):
  bot.add_cog(Fun(bot))