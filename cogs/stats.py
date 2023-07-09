from datetime import datetime, timedelta
from cogs.utils.constants import bot_color

from discord.ext import commands
import discord


class stats(commands.Cog):
    """displays some stats for the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong! 🏓", description=f"```md\n[{round(self.bot.latency * 1000)}ms]```", color=bot_color, timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

    def get_uptime(self):
        print(datetime.utcnow())
        return datetime.utcnow() - self.bot.start_time

    @commands.command(aliases=['ut'])
    async def uptime(self, ctx):
        """Shows how long the bot has been online for"""
        await ctx.send(self.bot.start_time)

        diff = self.get_uptime()

        embed = discord.Embed(title='<:online:876192917167964230> Uptime', color=bot_color, timestamp=datetime.utcnow(),
                              description=f"`{diff.days}` days, ` `hours, ` ` minutes, `{diff.seconds}` seconds")

        await ctx.send(embed=embed)

    @commands.command(aliases=['info'])
    async def about(self, ctx):
        """Shows some information about the bot"""
        pass


async def setup(bot):
    await bot.add_cog(stats(bot=bot))
