import sqlite3
from sqlite3 import Error
import discord
from discord.ext import commands
from discord.ext.commands import bot

#Connecting
def dbconnect(dbf):
  try:
    conn = sqlite3.connect(dbf)
  except Error:
    print(Error)
  else:
    return conn
db = dbconnect('setsuna.db')
cursor = db.cursor()

#Builds tables
async def deploy():
  cursor.execute("create table if not exists GuildConfig(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Prefix text, Welcome integer, WelcomeChannel integer, WelcomeMessage text)")
  cursor.execute("create table if not exists PBConfig(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Enabled integer, Channel integer, Count integer)")
  cursor.execute("create table if not exists PBLB(ID integer PRIMARY KEY AUTOINCREMENT, MemberID, Count integer)")
  cursor.execute("create table if not exists Log(ID integer PRIMARY KEY AUTOINCREMENT, GuildID, DelMsg, Ban, Kick, Clear)")
  cursor.execute("create table if not exists CountBlacklist(ID integer PRIMARY KEY AUTOINCREMENT, GuildID integer, Channel integer)")
  db.commit()

#Updates a cell of a given type from a guild (specified by ID)
async def update(table, cat, arg, guildid):
  cursor.execute("UPDATE "+table+" SET "+str(cat)+" = '"+str(arg)+"' WHERE GuildID = '"+str(guildid)+"'")
  db.commit()

#Selects and reads a cell
async def read(table, obj, guildid):
  cursor.execute("SELECT "+str(obj)+" FROM "+table+" WHERE GuildID='"+str(guildid)+"'")
  r = cursor.fetchall()
  return r