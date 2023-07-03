import random
from datetime import datetime
from PIL import Image, ImageColor

import discord
from discord.ext import commands


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

    # Send bot latency
    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        embed = discord.Embed(title='Pong! 🏓', description=f'```{round(self.bot.latency * 1000)}ms```',
                              color=0x2ecc71, timestamp=datetime.utcnow())
        add_author(embed, ctx.author)

        await ctx.send(embed=embed)

    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx):
        randint = random.randint(0, 1)

        embed = discord.Embed(title='Coinflip:', color=0x2ecc71, timestamp=datetime.utcnow())

        if randint == 0:
            embed.description = f'```Heads```'
            embed.set_image(url='https://cdn.discordapp.com/emojis/872621047525040129.png?v=1')
        elif randint == 1:
            embed.description = f'```Tails```'
            embed.set_image(url='https://cdn.discordapp.com/emojis/872621047449546772.png?v=1')

        await ctx.send(embed=embed)

    # Generates a random number from 0 to the given ceiling
    @commands.command(name='random', aliases=['rand', 'rng'])
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
            for i in range(1, int(ceiling) + 1):
                numcount += f'{i}: {nums.count(i)}\n'

            embed.add_field(name='Stats', value=f'```py\n{numcount}```', inline=False)

        embed.description = f'Generated `{repeat}` random integers from `1` to `{ceiling}`, inclusive\n```ini\n{nums}```'

        await ctx.send(embed=embed)

    # gets color given hex or rgb
    @commands.command(name="gcolor")
    async def getColor(self, ctx, arg):
        await ctx.send(arg)
        arg = int(arg, 16)
        print(type(arg))
        if type(arg) == int:
            h = arg
            rgb = ImageColor.getcolor(arg, "RGB")
        elif type(arg) == tuple and len(arg) == 3:
            h = '%02x%02x%02x' % arg
            rgb = arg
        else:
            await ctx.send("Invalid color argument")
            return

        img = Image.new("RGB", (300, 300), rgb)

        embed = discord.Embed(title=f"🎨 Information about the color **#{h}**")
        embed.add_field(name="Hex", value=f"{h}")
        embed.add_field(name="RGB", value=f"{rgb}")

        await ctx.send(f"{img}", embed=embed)

    # Purges a given number of messages
    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
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
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
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
    @commands.command(aliases=['sc'])
    async def skycrypt(self, ctx, ign, profile):
        await ctx.send(f'https://sky.shiiyu.moe/stats/{ign}/{profile}')

    @skycrypt.error
    async def skycrypt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention}, Please enter all required arguments')


def setup(bot):
    bot.add_cog(chatUtils(bot))
