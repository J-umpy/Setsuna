import discord
from discord.ext import commands
import traceback
import sys
import tools

#Thank you EvieePy for the generic error handler <3
class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Checks for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # Specific instructions for specific errors, if no instructions are found they're printed as the default traceback
        elif isinstance(error, commands.BadArgument):
            #if ctx.command.qualified_name == 'ban':   #Check if the command being invoked is 'ban'  ------ Ignore this, it's an example
            embed = tools.buildembed(ctx.command.qualified_name.title(), "Invalid Argument")
            await ctx.send(embed=embed)
        elif isinstance(error, discord.Forbidden):
            embed = tools.buildembed(ctx.command.qualified_name.title(), "I am missing the permissions required to perform this action")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotReadable):
            embed = tools.buildembed(ctx.command.qualified_name.title(), "I am missing the permissions to view this channel")
            await ctx.send(embed=embed)
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))