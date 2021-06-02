from discord.ext import commands
import tools
import sqlite3

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
  
    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, *, message = "** **"):
      if ctx.author.guild_permissions.manage_messages:
        await ctx.message.delete(delay=0.5)
        await ctx.send(message)
    @send.error
    async def sendcmd_handler(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        pass
    
    @commands.command()
    @commands.is_owner()
    async def joinsim(self, ctx):
      properties = (ctx.guild.id, '.', 0)
      tools.cursor.execute("INSERT INTO GuildConfig(GuildID, Prefix, TimeOutRole) VALUES(?, ?, ?)", properties)
      #tools.cursor.execute("INSERT INTO XP(GuildID, Member, ID, Count) VALUES(?, ?, ?, ?)", properties)
      properties = (ctx.guild.id, 0, 0, 0, 0, 0, 0)
      tools.cursor.execute("INSERT INTO Log(GuildID, DelMsg, Ban, Kick, Clear, Timeout, WordFilter) VALUES(?, ?, ?, ?, ?, ?, ?)", properties)
      tools.db.commit()
    @joinsim.error
    async def sendcmd_handler(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        pass


def setup(bot):
    bot.add_cog(OwnerCog(bot))