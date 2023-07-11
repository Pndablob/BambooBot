from cogs.utils.constants import bot_color

from discord.ext import commands
import discord


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['info'])
    async def about(self, ctx):
        """Shows some information about the bot"""
        pass


async def setup(bot):
    await bot.add_cog(Info(bot))
