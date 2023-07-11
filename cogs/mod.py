from cogs.utils.constants import bot_color

from discord.ext import commands
import discord


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Purged **{amount}** messages in {ctx.channel.mention}")

    @commands.command(aliases=['sm'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
    async def slowmode(self, ctx, delay: int):
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(f"Set the slowmode delay in {ctx.channel.mention} to `{delay}` seconds")


async def setup(bot):
    await bot.add_cog(Mod(bot))
