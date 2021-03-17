from discord.ext import commands


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
  
    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, *, message = "** **"):
      await ctx.message.delete(delay=0.5)
      await ctx.send(message)
    @send.error
    async def sendcmd_handler(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        pass

def setup(bot):
    bot.add_cog(OwnerCog(bot))