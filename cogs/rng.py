import math
import random
from datetime import datetime
from cogs.utils.constants import EMBED_COLOR

from discord.ext import commands
from discord import app_commands
import discord


class RNG(commands.Cog):
    """some psudo-rng commands"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='coinflip', description="Flips a coin")
    async def coinflip(self, interaction: discord.Interaction):
        """flips a coin"""
        randint = random.randint(0, 1)

        embed = discord.Embed(title='Coinflip:', color=EMBED_COLOR, timestamp=datetime.utcnow())

        if randint == 0:
            embed.description = f'```Heads```'
            embed.set_image(url='https://cdn.discordapp.com/emojis/872621047525040129.png?v=1')
        elif randint == 1:
            embed.description = f'```Tails```'
            embed.set_image(url='https://cdn.discordapp.com/emojis/872621047449546772.png?v=1')

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='random', description="Generates a list of random integers")
    @app_commands.describe(
        ceiling="upper bound of integers to generate",
        num="number of integers to generate",
        dupes="whether to generate duplicate integers",
        stats="whether to display frequency statistics",
    )
    async def random_number(self, interaction: discord.Interaction, ceiling: app_commands.Range[int, 0, 2**32], num: app_commands.Range[int, 1, 500] = 1, dupes: bool = False, stats: bool = False):
        """Return a list of random numbers, specifying a ceiling, duplicates, and statistics if within a certain limit"""
        nums = []
        numcount = ''

        # Checks if the repeats is larger than the ceiling, IFF duplicates are false
        if dupes is False and num > ceiling:
            num = ceiling

        embed = discord.Embed(color=EMBED_COLOR, timestamp=datetime.utcnow())

        # Runs generation until repeats reaches the given limit
        while len(nums) < num:
            randint = random.randint(0, ceiling)
            if dupes is True:
                nums.append(randint)
                embed.title = 'Result (with duplicates)'
            elif dupes is False:
                embed.title = 'Result (without duplicates)'
                while randint not in nums:
                    randint = random.randint(1, ceiling)
                    if randint not in nums:
                        nums.append(randint)

        # Show stats, if ceiling and num are within a certain limit
        if stats is True and (ceiling <= 50 and num <= 500) or (ceiling <= 100 and num <= 250):
            for i in range(1, ceiling + 1):
                numcount += f'{i}: {nums.count(i)}\n'

            embed.add_field(name='Stats', value=f'```py\n{numcount}```', inline=False)

        embed.description = f'Generated `{num}` random integers from `1` to `{ceiling}`, inclusive\n```ini\n{nums}```'

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(RNG(bot))

