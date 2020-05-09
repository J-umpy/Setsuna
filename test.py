import sqlite3
from sqlite3 import Error
import discord
from discord.ext import commands
from discord.ext.commands import bot
def dbconnect(dbf):
  try:
    conn = sqlite3.connect(dbf)
  except Error:
    print(Error)
  else:
    return conn
db = dbconnect('setsuna.db')
cursor = db.cursor()
def buildtable():
  cursor.execute("create table if not exists GuildConfig(ID integer PRIMARY KEY, GuildID integer, Prefix text, Welcome integer, WelcomeChannel integer, WelcomeMessage text, WordFilter integer, Pineappleboard integer)")
  #Add logs as their own table
  #Add pineappleboard as it's own table + a table for leaderboards
  #Token and owners can be in JSON indefinitely
  #Blacklisted channels should probably be their own databases as well
  db.commit()
buildtable()

bot = commands.Bot(command_prefix="!", case_insensitive=True, help_command=None)

@bot.event
async def on_guild_join(guild):
  cursor.execute('SELECT ID FROM GuildConfig WHERE ID = (SELECT MAX(ID) FROM GuildConfig)')
  #ID = cursor.fetchall()
  ID = 0
  #int(ID[0])
  msg = "{MENTION} has joined the server"
  properties = (ID+1, guild.id, None, 0, 0, msg, 0, 0)
  cursor.execute("INSERT INTO GuildConfig(ID, GuildID, Prefix, Welcome, WelcomeChannel, WelcomeMessage, WordFilter, Pineappleboard) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", properties)
  db.commit()
bot.run('token here')