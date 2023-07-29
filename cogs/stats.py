import math
from datetime import datetime
from cogs.utils.constants import EMBED_COLOR

from discord.ext import commands
from discord import app_commands
import discord


class Stats(commands.Cog):
    """displays some stats for the bot"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Pong! 🏓", description=f"```md\n[{round(self.bot.latency * 1000)}ms]```",
                              color=EMBED_COLOR, timestamp=datetime.now())
        await interaction.response.send_message(embed=embed)

    def get_uptime(self):
        return round(datetime.timestamp(datetime.utcnow()) - datetime.timestamp(self.bot.start_time))

    @app_commands.command(name="uptime")
    async def uptime(self, interaction: discord.Interaction):
        """Shows how long the bot has been online for"""
        diff = self.get_uptime()  # seconds since startup

        days = math.floor(diff / 86400)  # Floor of diff / sec-in-day (86400)
        hours = math.floor((diff % 86400) / 3600)  # Floor of (diff mod sec-in-day) / sec-in-hour (3600)
        minutes = math.floor((diff % 3600) / 60)  # Floor of (diff mod sec-in-hour) / sec-in-min (60)
        seconds = (diff % 60)  # diff mod sec-in-min

        embed = discord.Embed(title='<:online:1127821209921400833> Uptime', color=EMBED_COLOR, timestamp=datetime.now(),
                              description=f"`{days}` days, `{hours}`hours, `{minutes}` minutes, `{seconds}` seconds")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot=bot))
