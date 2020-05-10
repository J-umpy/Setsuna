import discord
from discord.ext import commands
from discord.ext.commands import bot, TextChannelConverter
import random
import json
import asyncio
import cfg
import urllib
class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  async def qmath(self, ctx, loop, num, rannum):
    rannum = rannum + num
    def chck(m):
      return m.channel == ctx.channel and m.author.bot != True
    try:
      msg = await self.bot.wait_for('message', timeout=10, check=chck)
    except asyncio.TimeoutError:
      embed = cfg.buildembed('Mini Bonus!', "Timed out, let's go back to the main game!")
    try:
      msg = int(msg.content)
    except:
      embed = cfg.buildembed('Mini Bonus!', "That's not even a number, back to the main game!", discord.Colour.red())
    if msg == rannum:
      loop += 5
      embed = cfg.buildembed('Mini Bonus!', f'You win!\nYour score is now {loop}\nLast recorded number: {num-1}', discord.Colour.green())
    else:
      embed = cfg.buildembed('Mini Bonus!', f"You lose! \nThe answer was {rannum}\nYour score is {loop}, now let's get back to it\nLast recorded number: {num-1}", discord.Colour.red())
    await ctx.send(embed=embed)
    return loop, num

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
        embed = cfg.buildembed('Bonus Time!', "Timed Out, let's go back to the main game!")
      try:
        msg = int(msg.content)
      except:
        tries = tries - 1
        embed = cfg.buildembed('Bonus Time!', f'Your guess was invalid. {tries} tries remaining')
        continue
      else:
        if msg > ans:
          tries = tries - 1
          embed = cfg.buildembed('Bonus Time!', f'The number is lower\n {tries} tries remaining')
        elif msg < ans:
          tries = tries - 1
          embed = cfg.buildembed('Bonus Time!', f'The number is higher\n {tries} tries remaining')
        else:
          loop = loop + loop
          embed = cfg.buildembed('Bonus Time!', f'You win!\nYour score is now {loop}\nLast recorded number: {num-1}', discord.Colour.green())
          await ctx.send(embed=embed)
          break
    if tries == 0:
      embed = cfg.buildembed('Bonus Game!', f'You lost!\nThe number was {ans}.\nYour score is {loop}, now back to The Counting Game! Last recorded number: {num-1}', discord.Colour.red())
      await ctx.send(embed=embed)
    return loop, num

  @commands.group(aliases=['countinggame', 'counting'])
  async def count(self, ctx):
    if ctx.invoked_subcommand == None:
      if not ctx.channel.id in cfg.data['countblacklist'] or ctx.message.author.guild_permissions.manage_messages == True:
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
            embed = cfg.buildembed('Counting Game', f'No one sent a message for 10 seconds, so the game ended. Your score was {loop}')
            await ctx.send(embed=embed)
            break
          else:
            if message.content != num:
              embed = cfg.buildembed('Counting Game', f'Game Over! Your score is {loop}')
              await ctx.send(embed=embed)
              break
            else:
              loop += 1
              num = int(num)
              num += 1
              if random.randint(1, 25) == 10:
                #embed = cfg.buildembed('Bonus Time!', f'If you successfully complete the bonus challenge, your score of {loop} will be doubled!')
                #await ctx.send(embed=embed)
                embed = cfg.buildembed('Bonus Time!', "Guess what number I am thinking of! It's between 1 and 100, inclusive")
                loop, num = await Fun.numberguessing(self, ctx, loop, embed, num)
              elif random.randint(1, 10) == 2:
                rannum = random.randint(-100, 100)
                if rannum < 0:
                  embed = cfg.buildembed('Mini Bonus!', f"Quickly subtract {abs(rannum)} from {num-1}!")
                else:
                  embed = cfg.buildembed('Mini Bonus!', f"Quickly add {rannum} to {num-1}!")
                await ctx.send(embed=embed)
                loop, num = await Fun.qmath(self, ctx, loop, num-1, rannum)


  @count.command(aliases=['bl'])
  async def blacklist(self, ctx, channel):
    if ctx.author.guild_permissions.manage_channels == True:
      try:
        channel = await TextChannelConverter().convert(ctx, str(channel))
      except:
        embed = cfg.buildembed('Count Blacklist', 'Channel could not be found')
        await ctx.channel.send(embed=embed)
      else:
        if channel.id in cfg.data['countblacklist']:
          cfg.data['countblacklist'].remove(channel.id)
          with open('config.json', 'w') as f:
            json.dump(cfg.data, f, indent=4)
          embed = cfg.buildembed('Count Blacklist', f'Successfully unblacklisted {channel.mention}')
          await ctx.send(embed=embed)
        else: 
          cfg.data['countblacklist'].append(channel.id)
          with open('config.json', 'w') as f:
            json.dump(cfg.data, f, indent=4)
          embed = cfg.buildembed('Count Blacklist', f'{channel.mention} has been successfully blacklisted')
          await ctx.send(embed=embed)
    else:
      embed = cfg.buildembed('Count Blacklist', 'This command requires the manage channels permission')
      await ctx.send(embed=embed)
    
  @commands.command()
  async def say(self, ctx, *, message = None):
    if ctx.author.guild_permissions.manage_messages == True:
      if message != None or len(ctx.message.attachments) != 0:
        embed = cfg.buildembed(self.bot.user.name, message)
        if len(ctx.message.attachments) > 0:
          embed.set_image(url=ctx.message.attachments[0].url)
        await ctx.message.delete(delay=0.5)
        await ctx.send(embed=embed)

  @commands.command()
  async def inspire(self, ctx):
    request = urllib.request.Request("https://inspirobot.me/api?generate=true", None,{'User-Agent':"Opera"})
    embed = cfg.buildembed("Feel Inspired", "")
    request =str(urllib.request.urlopen(request).read().decode('UTF-8'))
    embed.set_image(url=request)
    embed.set_footer(text="Brought to you by Inspirobot")
    await ctx.send(embed = embed)


def setup(bot):
  bot.add_cog(Fun(bot))
