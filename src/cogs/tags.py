from datetime import datetime

import discord
from discord.ext import commands


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tags')
    @commands.is_owner()
    async def _tags(self, ctx):
        tags_list = []

        

        embed = discord.Embed(title='Tags', color=0x2ecc71, timestamp=datetime.utcnow())

    @commands.command(name='winner')
    @commands.has_any_role(
        # PBT
        815952833253605426,  # *
        # BB
        472842678778724352,  # Intellectual
        648208270988673062,  # Giveaways
    )
    async def winner(self, ctx):
        giveaway_channels = [
            783757332333068288,  # giveaways channel, BB
            754868244489306122,  # epic-ppl-giveaways channel, BB
            ]
        time = '24 hours'

        # Delete command
        await ctx.message.delete()

        if ctx.channel.id in giveaway_channels:
            if ctx.channel == 754868244489306122:
                time = '48 hours'
        elif await self.bot.is_owner(ctx.author):
            pass
        else:
            await ctx.send('Please use this tag in a giveaway channel')
            return

        embed = discord.Embed(title='A giveaway has ended 🎉!', color=0x2ecc71, timestamp=datetime.utcnow(),
                              description=f'Congratulations! The winner(s) may DM {ctx.author.mention} with their IGN **within {time}** to claim their prize(s)!')
        add_author(embed, ctx.author)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(tags(bot))
