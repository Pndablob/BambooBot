from datetime import datetime

import discord
from discord.ext import commands


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class userUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Echos a message
    @commands.command(aliases=['say'])
    @commands.is_owner()
    async def echo(self, ctx, *, msg):
        await ctx.message.delete()

        ch = self.bot.get_channel(850159250629722123)
        embed = discord.Embed(title='Echo 📣', description=f'Echoed message by {ctx.message.author.mention}\n',
                              color=0x2ecc71, timestamp=datetime.utcnow())
        embed.add_field(name='Message:', value=f'```{msg}```', inline=False)
        embed.add_field(name='Guild:', value=f'```{ctx.message.guild}```', inline=False)

        await ctx.send(msg)
        await ch.send(embed=embed)

    # DM's a user a message
    @commands.command(name='message', aliases=['dm', 'poke'])
    @commands.is_owner()
    async def _message(self, ctx, user: discord.Member, *, msg):
        await ctx.message.delete()
        await user.send(msg)

        ch = self.bot.get_channel(850159250629722123)
        embed = discord.Embed(title='Boop! ❗', description=f'{user.mention} was poked', color=0x2ecc71,
                              timestamp=datetime.utcnow())
        embed.add_field(name='Message:', value=f'```{msg}```', inline=False)
        embed.add_field(name='Guild:', value=f'```{ctx.message.guild}```', inline=False)
        await ch.send(embed=embed)

    # Listens for a DM'ed response to the bot
    @commands.Cog.listener("on_message")
    @commands.is_owner()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel) or message.author.id == self.bot.user.id:
            # not a DM, or it's just the bot itself
            return

        channel = self.bot.get_channel(864003007389630535)
        author = message.author
        content = message.clean_content

        # If content contains a message
        msg_embed = discord.Embed(title=f'Reply from `{author.name}#{author.discriminator}`',
                                  timestamp=message.created_at, color=author.color)
        msg_embed.set_author(name=f'{author.id}', icon_url=author.avatar_url)
        signature(msg_embed)

        # If message contains chars
        if len(content) > 0:
            msg_embed.add_field(name='Message', value=f'```{content[:1018]}```', inline=False)
        # If message is longer than 1018 chars
        elif len(content[1018:]) > 0:
            msg_embed.add_field(name='(Continued)', value=f'```{content[1018:2036]}```', inline=False)
        # If message is longer than 2036 chars
        elif len(content[2036:]) > 0:
            msg_embed.add_field(name='(Continued)', value=f'```{content[2036:3054]}```', inline=False)
        # If message is longer than 3054 chars
        elif len(content[3054:]) > 0:
            msg_embed.add_field(name='(Continued)', value=f'```{content[3054:4072]}```', inline=False)
        await channel.send(content=f'{author.id}', embed=msg_embed)

        if message.attachments is not None:
            for attachments in message.attachments:
                await channel.send(attachments)

        await self.bot.process_commands(message)

    # Sends info about a user
    @commands.command(pass_context=True)
    @commands.is_owner()
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
    bot.add_cog(userUtils(bot))