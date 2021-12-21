import discord
from discord.ext import commands


class math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Converts numbers from base 10
    @commands.command(name='convertBase', aliases=['convbase', 'cb'])
    async def convertBase(self, ctx, base: int, num: int):
        if base <= 0:
            await ctx.send('Please enter a positive base')
            return
        elif base == 2:
            await ctx.send(f'Base 10 `{num}` to base `{base}` is: `{bin(num)}`')
        elif base == 8:
            await ctx.send(f'Base 10 `{num}` to base `{base}` is: `{oct(num)}`')
        elif base == 16:
            await ctx.send(f'Base 10 `{num}` to base `{base}` is: `{hex(num)}`')


def setup(bot):
    bot.add_cog(math(bot))
