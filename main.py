import discord
from discord.ext.commands import bot
from discord.ext import commands
import os, sys, traceback, asyncio
import random
from numpy.random import choice
bot = commands.Bot(command_prefix=".")
Token = "NTU2Njc0OTY0ODI1MzA5MTg0.D3GL1Q.h2XD5C4FLW1C9EZJnqVTxH_kWnw"
@bot.event
async def on_ready():
    print('Ready Player Setsuna\n- - - - - - - ')


@bot.command(aliases = ["b"])
async def ban(ctx, member:discord.User = None, Prereason = None):
  Message = ctx.message.content
  CommandPrefix = ctx.prefix
  CommandAlias = ctx.invoked_with
  if ctx.message.author.guild_permissions.ban_members == False:
    if member == None:
      await ctx.channel.send(random.choice(["Not only are you missing permissions, but you also messed up the command!", "You're missing something, and some permissions too", "I'd correct you, but you're not even supposed to use this command", "pat, pat"]))
    else:
      await ctx.channel.send(random.choice(["No.", "I apologise, but I cannot accept that command from you.", "I don't mean to be rude, but you aren't authorized to use that command", "Jumpy has not deemed you worthy of that command. Hopefully you'll be ready one day!"]))
  if ctx.message.author.guild_permissions.ban_members:
    if ctx.message.author.guild_permissions.ban_members:
        if ctx.message.author.id == 171330866189041665 and member.id != 385991322693009421:
            print("Neeko was a bad boi >:C")
            return
        if member == None:
            BanNoUserSpecifiedError = random.choice(["I cannot ban nothing.", "There isn't anything there...", "No user was found.", "Did you forget something?", "Try that ban again, sweetie."])
            await ctx.channel.send(BanNoUserSpecifiedError)
        elif member == ctx.message.author:
            BanSelfBanError = random.choice(["Why are you trying to ban yourself?", "I cannot allow you to harm yourself", "I won't hurt you!", "Why...?", "How about I heal you instead?", "I don't want you to go :c"])
            await ctx.channel.send(BanSelfBanError)
            return
        else:
            if Prereason == None:
              reason = "No reason given, please ask the Admin responsible to submit a reason"
            else:
              PreReason2 = Message[len(CommandPrefix) + len(CommandAlias):]
              reason = f'ID: {PreReason2}'
              Message = f'You have been banned from {ctx.guild.name}. \n reason: {reason}\n User:{ctx.message.author}'
            try:
                await member.send(Message)
            except(discord.Forbidden):
                'Error: Missing Permissions'
                #await ctx.channel.send(f"<@{member.id}> has server DMs disabled - They will not recieve any messages about the ban.")
            try:
                await ctx.guild.ban(member, reason=reason, delete_message_days=0)
                await ctx.channel.send(f'A user has been banned. {reason}')
            except(discord.Forbidden):
                await ctx.channel.send("I apologize, I do not have the permissions to do this.")
    else:
        await ctx.channel.send(random.choice(["No.", "I apologise, but I cannot accept that command from you.", "I don't mean to be rude, but you aren't authorized to use that command", "Jumpy has not deemed you worthy of that command. Hopefully you'll be ready one day!"]))

@bot.command(aliases = ["dye", "bye", "banthebot"])
async def shutdown(ctx):
    if ctx.message.author.id == 291353858301624320:
        await ctx.channel.send("The Pilgrimage Ended in Failure...")
        await bot.change_presence(status = discord.Status.dnd, activity = discord.Game("Dying..."))
        await asyncio.sleep(3)
        sys.exit("Called upon by one of the Owners")


@bot.command(aliases = ["setp"])
async def setpresence(ctx, BotStatus):
  if ctx.message.author.id == 291353858301624320:
    if BotStatus.upper() == "ONLINE":
      await bot.change_presence(status = discord.Status.online)
      await ctx.channel.send("I summon Setsuna in face-up attack mode!")
    elif BotStatus.upper() == "IDLE":
      await bot.change_presence(status = discord.Status.idle)
      await ctx.channel.send("Getting into idle position...")
    elif BotStatus.upper() == "DND":
        await bot.change_presence(status = discord.Status.dnd)
        await ctx.channel.send("Now my presence matches my hair!")
    elif BotStatus.upper() == "OFFLINE":
        await bot.change_presence(status = discord.Status.offline)
        await ctx.channel.send("I'm like a ghost now!")
  else:
    await ctx.channel.send("I don't know if I trust your recommendations.")


@bot.command(aliases=["seta"])
async def setactivity(ctx, Type = None,):
  Message = ctx.message.content
  CommandPrefix = ctx.prefix
  CommandAlias = ctx.invoked_with
  PreBA1 = Message[len(CommandPrefix) + len(CommandAlias) + len(Type):]
  PreBA2 = PreBA1.lstrip('g')
  BA = PreBA2.lstrip('')
  if Type.upper() == "WATCH" or Type.upper() == "WATCHING":
   await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=BA.lstrip('h')))
   await ctx.channel.send("That looks interesting, I'll check it out!")
  elif Type.upper() == "PLAY" or Type.upper() == "PLAYING" or Type.upper() == "GAME":
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=BA.lstrip('e')))
    await ctx.channel.send("That game looks fun, I'll play it!")
  elif Type.upper() == "STREAM" or Type.upper() == "STREAMING":
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=BA.lstrip('m')))
    await ctx.channel.send("I'll take the internet by storm with this stream!")
  elif Type.upper() == "LISTEN" or Type.upper() == "LISTENING":
     await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=BA.lstrip('n')))
     await ctx.channel.send("I'm all ears!")

@bot.command(aliases = ["delete", "purge", "d", "p"])
async def clear(ctx, Amount, User:discord.User = None):
    amount = int(Amount)
    if ctx.message.author.guild_permissions.manage_messages:
        if amount > 99:
            DeleteTooManyMessagesError = random.choice(["I apologise, but I can't handle deleting that many messages :c"] ["I am not strong enough to handle that many messages at once.", "Maybe with some training, I can delete more than 99 messages", "If I could delete over 99 messages, I would delete over 99 messages"])
            await ctx.channel.send(DeleteTooManyMessagesError)
        elif amount < 1:
            DeleteNoMessagesError = random.choice(["I agree, no messages should be deleted. ^-^", "These messages are safe... for now...", "Phew, when you typed that command I was worried I might have to delete something." "BulletBot might have deleted that, but I wouldn't.", "If you're looking to mess around, Gambling Bot and Discord Miner are better for that. My sister is pretty fun too!"])
            await ctx.channel.send(DeleteNoMessagesError)
        else:
          await ctx.channel.purge(limit=amount, bulk=True)
          DeleteMessagesSuccess = random.choice(["Deletion Completion!", "I miss those messages already...", "I hope none of those messages were mine.", "If any of those bad messages come back, let me know.", "If only those messages and I could have talked things out...", "Setsuna is on the job.", "Those messages won't be bothering you anymore.", "With great power comes great responsibility.", "I hope I didn't miss any.", "I hope none of those messages were important.", "Let's talk things out next time.", "I wish I could have saved those messages, but you guys are more important", "Please don't use this power too often", "I feel bad for BulletBot." "Poor BulletBot won't be able to log all of these messages."])
          await ctx.channel.send(DeleteMessagesSuccess)
    else:
        DeleteMissingPermissionsError = random.choice(["You're missing a few permissions.", "Deletion Completi- never mind... :c", "With great power comes great responsibility. You have neither.", "It's my mission to protect you from the dangerous powers of deletion.", "I musn't allow you to turn to the dark side, this command will not be executed.", "No.", "If I take orders from you, I can't protect you as well.", "My mission is to protect, I musn't misuse my power", "Messages, you can live on another day.", "Maybe if you ask nicely, the messages will delete themselves!", "How about we talk things out with the messages instead.", "You're unauthorized to give me that command, try asking Mao?", "You're unauthorized to give me that command. BulletBot, take them away.", "Mao, watch out, these guys are trying to use commands they shouldn't be using."])
        await ctx.channel.send(DeleteMissingPermissionsError)

@bot.command()
async def coin(ctx):
  Coin = ["It's heads!", "It's tails!", ":00000, it landed on it's side!"]
  Weights = [.49, .49, .02]
  await ctx.channel.send(choice(Coin, p=Weights))

#@bot.command()
#async def echo(ctx, CHID):
  #if ctx.message.author.id == 291353858301624320:
    #channel = bot.get_channel(CHID)
    #Message = ctx.message.content
    #CommandPrefix = ctx.prefix
    #CommandAlias = ctx.invoked_with
    #Echoed = Message[len(CommandPrefix) + len(CommandAlias):]
    #await channel.send(Echoed)


#@bot.command(aliases = ["echo"])
#async def repeat(ctx):
  #Message = ctx.message.content
  #CommandPrefix = ctx.prefix
  #CommandAlias = ctx.invoked_with
  #Echoed = Message[len(CommandPrefix) + len(CommandAlias):]
  #await ctx.send(content=f"{Echoed}")


bot.run(Token)


