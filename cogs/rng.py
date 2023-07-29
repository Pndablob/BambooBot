import random
from datetime import datetime

from cogs.utils.constants import EMBED_COLOR
from cogs.utils.messages import add_author

from discord.ext import commands
import discord


class RNG(commands.Cog):
    """some psudo-rng commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coinflip', aliases=['cf'])
    async def coinflip(self, ctx):
        """flips a coin"""
        randint = random.randint(0, 1)

        embed = discord.Embed(title='Coinflip:', color=EMBED_COLOR, timestamp=datetime.utcnow())

        if randint == 0:
            embed.description = f'```Heads```'
            embed.set_image(url='https://cdn.discordapp.com/emojis/872621047525040129.png?v=1')
        elif randint == 1:
            embed.description = f'```Tails```'
            embed.set_image(url='https://cdn.discordapp.com/emojis/872621047449546772.png?v=1')

        await ctx.send(embed=embed)

    @commands.command(name='random', aliases=['rand', 'randnum', 'number', 'num'])
    async def random_number(self, ctx, ceiling: int = 10, repeat: int = 1, dupes=False, stats=False):
        """Return a list of random numbers, specifying a ceiling, duplicates, and statistics if within a certan limit"""
        nums = []
        numcount = ''

        # Checks if the repeats is larger than the ceiling, IFF duplicates are false
        if dupes is False and repeat > ceiling:
            await ctx.send(
                f'Duplicates were not requested and repeats is greater than the ceiling. Repeats has been set to the maximum allowed.')
            repeat = ceiling

        embed = discord.Embed(color=EMBED_COLOR, timestamp=datetime.utcnow())
        add_author(embed, ctx.author)

        # Runs generation until repeats reaches the given limit
        while len(nums) < repeat:
            randint = random.randint(1, ceiling)
            if dupes is True:
                nums.append(randint)
                embed.title = 'Result (with duplicates)'
            elif dupes is False:
                embed.title = 'Result (without duplicates)'
                while randint not in nums:
                    randint = random.randint(1, ceiling)
                    if randint not in nums:
                        nums.append(randint)

        # Show stats, if ceiling and repeats are within a certain limit
        if stats is True and (ceiling <= 50 and repeat <= 500) or (ceiling <= 100 and repeat <= 250):
            for i in range(1, ceiling + 1):
                numcount += f'{i}: {nums.count(i)}\n'

            embed.add_field(name='Stats', value=f'```py\n{numcount}```', inline=False)

        embed.description = f'Generated `{repeat}` random integers from `1` to `{ceiling}`, inclusive\n```ini\n{nums}```'

        add_author(embed, ctx.author)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RNG(bot))

