import random
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext import tasks


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class chatUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkup.start()

    # Send bot latency
    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f'```md\n# Pong!\n{round(self.bot.latency * 1000)}ms```')

    @tasks.loop(hours=1)
    async def checkup(self):
        ch = self.bot.get_channel(820473911753310208)
        embed = discord.Embed(description=f'```md\n# Ping:\n{round(self.bot.latency * 1000)}ms```', color=0x2ecc71,
                              timestamp=datetime.utcnow())
        signature(embed)

        await ch.send(embed=embed)

    # Generates a random number from 0 to the given ceiling
    @commands.command(name='random', aliases=['rand'])
    @commands.is_owner()
    async def random_number(self, ctx, ceiling, repeat=1, dupes=False, stats=True):
        nums = []
        numcount = ''

        # Checks if the repeats is larger than the ceiling, IFF duplicates are false
        if dupes is False and int(repeat) > int(ceiling):
            await ctx.send(f'Duplicates were not requested and repeat was greater than the ceiling. Repeats has been set to the maximum allowed.')
            repeat = ceiling

        embed = discord.Embed(color=0x2ecc71, timestamp=datetime.utcnow())
        add_author(embed, ctx.author)

        # Runs generation until repeats reaches the given limit
        while len(nums) < int(repeat):
            randint = random.randint(1, int(ceiling))
            if dupes is True:
                nums.append(randint)
                embed.title = 'Result (with duplicates)'
            elif dupes is False:
                embed.title = 'Result (without duplicates)'
                while randint not in nums:
                    randint = random.randint(1, int(ceiling))
                    if randint not in nums:
                        nums.append(randint)

        # Show stats, if ceiling and repeats are within a certain limit
        if stats is True and ((int(ceiling) <= 50 and int(repeat) <= 500) or (int(ceiling) <= 100 and int(repeat) <= 250)):
            for i in range(1, int(ceiling)+1):
                numcount += f'{i}: {nums.count(i)}\n'

            embed.add_field(name='Stats', value=f'```py\n{numcount}```', inline=False)

        embed.description = f'Generated `{repeat}` random integers from `1` to `{ceiling}`, inclusive\n```ini\n{nums}```'

        await ctx.send(embed=embed)

    # Purges a given number of messages
    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.is_owner()
    async def clear(self, ctx, amount):
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send(f'Purged **{amount}** messages in {ctx.channel.mention}')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.message.author.mention}, You do not have permission to use this command')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention}, Please enter all required arguments')
        else:
            raise error

    # Sets the slowmode of a channel
    @commands.command(aliases=['sm'])
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
    @commands.is_owner()
    async def slowmode(self, ctx, delay: int):
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(f'Set the slowmode delay in {ctx.channel.mention} to `{delay}` seconds')

    @slowmode.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.message.author.mention}, You do not have permission to use this command')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention}, Please enter all required arguments')
        else:
            raise error

    # sky.shiiyu.moe command
    @commands.command(aliases=['sc', 'scs'])
    @commands.is_owner()
    async def skycrypt(self, ctx, ign, profile):
        await ctx.send(f'https://sky.shiiyu.moe/stats/{ign}/{profile}')

    @skycrypt.error
    async def skycrypt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention}, Please enter all required arguments')


def setup(bot):
    bot.add_cog(chatUtils(bot))
