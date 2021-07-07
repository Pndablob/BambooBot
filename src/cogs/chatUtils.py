from datetime import datetime
import discord
from discord.ext import commands


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Send bot latency
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms`')


class purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Purges a given number of messages
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command()
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


class slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sets the slowmode of a channel
    @commands.command(aliases=['sm'])
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, delay: int):
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(f'Set the slowmode delay in {ctx.channel.mention} to {delay} seconds')


class skycrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # sky.shiiyu.moe command
    @commands.command(aliases=['sc', 'scs'])
    async def skycrypt(self, ctx, ign, profile):
        await ctx.send(f'https://sky.shiiyu.moe/stats/{ign}/{profile}')


def setup(bot):
    bot.add_cog(ping(bot))
    bot.add_cog(purge(bot))
    bot.add_cog(slowmode(bot))
    bot.add_cog(skycrypt(bot))
