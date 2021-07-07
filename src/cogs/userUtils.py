from datetime import datetime
import discord
from discord.ext import commands


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Echos a message
    @commands.command(aliases=['say'])
    async def echo(self, ctx, *, msg):
        await ctx.message.delete()

        ch = self.bot.get_channel(850159250629722123)
        embed = discord.Embed(title='Echo 📣', description=f'Echoed message by {ctx.message.author.mention}\n',
                              color=0x2ecc71, timestamp=datetime.utcnow())
        embed.add_field(name='Message:', value=f'```{msg}```', inline=False)
        embed.add_field(name='Guild:', value=f'```{ctx.message.guild}```', inline=False)

        await ch.send(embed=embed)


class dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # DM's a user a message
    @commands.command(name='message', aliases=['dm', 'poke'])
    async def _message(self, ctx, user: discord.Member, *, msg):
        await ctx.message.delete()
        await user.send(msg)

        ch = self.bot.get_channel(850159250629722123)
        embed = discord.Embed(title='Boop! ❗', description=f'{user.mention} was poked', color=0x2ecc71,
                              timestamp=datetime.utcnow())
        embed.add_field(name='Message:', value=f'```{msg}```', inline=False)
        embed.add_field(name='Guild:', value=f'```{ctx.message.guild}```', inline=False)
        await ch.send(embed=embed)


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sends info about a user
    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        fields = [
            ('Username', user.mention, False),
            ('User ID', user.id, False),
            ('Highest Role', user.top_role, False),
            ('Create Date', user.created_at, False),
            ('Join Date', user.joined_at, False)
        ]
        embed = discord.Embed(title='User Info:', color=0x0565ff, timestamp=datetime.utcnow())
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(echo(bot))
    bot.add_cog(dm(bot))
    bot.add_cog(info(bot))
