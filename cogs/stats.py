import math
from datetime import datetime
from cogs.utils.constants import bot_color

from discord.ext import commands
import discord


class Stats(commands.Cog):
    """displays some stats for the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong! 🏓", description=f"```md\n[{round(self.bot.latency * 1000)}ms]```",
                              color=bot_color, timestamp=datetime.now())
        await ctx.send(embed=embed)

    def get_uptime(self):
        print(datetime.utcnow())
        return round(datetime.timestamp(datetime.utcnow()) - datetime.timestamp(self.bot.start_time))

    @commands.command(aliases=['ut'])
    async def uptime(self, ctx):
        """Shows how long the bot has been online for"""
        diff = self.get_uptime()  # seconds since startup

        days = math.floor(diff / 86400)  # Floor of diff / sec-in-day (86400)
        hours = math.floor((diff % 86400) / 3600)  # Floor of (diff mod sec-in-day) / sec-in-hour (3600)
        minutes = math.floor((diff % 3600) / 60)  # Floor of (diff mod sec-in-hour) / sec-in-min (60)
        seconds = (diff % 60)  # diff mod sec-in-min

        embed = discord.Embed(title='<:online:1127821209921400833> Uptime', color=bot_color, timestamp=datetime.now(),
                              description=f"`{days}` days, `{hours}`hours, `{minutes}` minutes, `{seconds}` seconds")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot=bot))
