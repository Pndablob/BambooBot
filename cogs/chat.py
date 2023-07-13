from datetime import datetime

from discord.ext import commands
from discord import app_commands
import discord


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stealemote', aliases=['steal', 'yoink'])
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def steal_emote(self, ctx, emoji: discord.Emoji, *, name: str):
        """hippity hoppity your emoji is now my property"""
        pass

    @commands.command(name='echo', aliases=['e'])
    async def echo(self, ctx, *, msg):
        """echos a message"""
        await ctx.message.delete()
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Chat(bot))
