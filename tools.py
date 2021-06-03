import json
import discord
import os
with open('config.json') as f:
  data = json.loads(f.read())
#Fetches a list of cogs for use in the launcher and help command. Thank you to Neeko_iko for introducing me to the OS module <3
async def fetch_cogs():
  cogs = []
  files = os.listdir('./cogs')
  for i in files:
    if i.endswith('.py'):
      i = i.replace('.py', '')
      cogs.append(i)
  return cogs
#Closes and re-opens config.json, resyncing the data in the RAM with what's written to the disk
async def cfgreload():
  global data
  with open('config.json') as f:
    data = json.loads(f.read())
#An embed creator. It has default arguments so if I forget something an error isn't raised
def buildembed(title = "Placeholder Title", description = "Placeholder Description", colour = discord.Colour.from_rgb(251, 217, 229)):
  embed = discord.Embed(title=title, description=description, colour=colour)
  return embed

import sqlite3
from sqlite3 import Error
import discord
from discord.ext import commands
from discord.ext.commands import bot

# XP Queue Initialization
# pending = {}
# async def queueinit():
#   guilds = bot.guilds
#   pending = {}
#   for guild in guilds:
#     pending[guild.id] = {}
# queueinit()

# DATABASE STUFF

#Connecting
def dbconnect(dbf):
  try:
    conn = sqlite3.connect(dbf, cached_statements=500)
  except Error:
    print(Error)
  else:
    return conn
db = dbconnect('setsuna.db')
cursor = db.cursor()

#Builds tables
async def deploy():
  cursor.execute("create table if not exists GuildConfig(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Prefix text, TimeOutRole integer, XP enabled)")
  cursor.execute("create table if not exists XP(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Count integer, Next integer, Level integer)")
  cursor.execute("create table if not exists Log(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, DelMsg integer, Ban integer, Kick integer, Clear integer, Timeout integer, WordFilter integer)")
  cursor.execute("create table if not exists CountBlocklist(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Channel integer)")
  cursor.execute("create table if not exists CommandBlocklist(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Channel integer)")
  cursor.execute("create table if not exists WordFilter(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Word text)")
  db.commit()

#Updates a value in a given table
async def update(table, cat, arg, guildid):
  cursor.execute("UPDATE "+table+" SET "+str(cat)+" = '"+str(arg)+"' WHERE GuildID = '"+str(guildid)+"'")
  db.commit()

#Reads a value from a given table
async def read(table, obj, guildid):
  cursor.execute("SELECT "+str(obj)+" FROM "+table+" WHERE GuildID='"+str(guildid)+"'")
  r = cursor.fetchall()
  return r