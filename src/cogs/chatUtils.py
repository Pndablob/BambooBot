from datetime import datetime

import discord
from discord.ext import commands


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class chatUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Send bot latency
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms`')

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
        await ctx.send(f'Set the slowmode delay in {ctx.channel.mention} to {delay} seconds')

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
    async def skycrypt(self, ctx, ign, profile):
        await ctx.send(f'https://sky.shiiyu.moe/stats/{ign}/{profile}')

    @skycrypt.error
    async def skycrypt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention}, Please enter all required arguments')


def setup(bot):
    bot.add_cog(chatUtils(bot))
