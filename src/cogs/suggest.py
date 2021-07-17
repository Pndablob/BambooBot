import discord
from discord.ext import commands
from datetime import datetime


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Suggestion command
    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 7200)
    async def suggest(self, ctx, sugtype=None, *, suggestion=None):
        # Gets channels for waitlist, logging, and approved suggestions
        suggestionLogsChannel = self.bot.get_channel(851221149378805802)
        suggestionWaitlistChannel = self.bot.get_channel(844926347599151154)
        suggestionApproveChannel = self.bot.get_channel(851204911533785088)

        def check(reaction, user):
            return user == ctx.message.author

        if suggestion is None:
            suggestion = 'Empty Suggestion'

        # Suggestion for SBA
        if sugtype == 'sba':
            await ctx.message.add_reaction('✅')

            # Creates embedded message for a suggestion
            sbaSuggestionEmbed = discord.Embed(title=f'New SBA Suggestion by {ctx.message.author}',
                                               description=f'```{suggestion}```', color=0xF5A623,
                                               timestamp=datetime.utcnow())
            signature(embedMessage=sbaSuggestionEmbed)
            sbaSuggestionEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

            # Sends embed in the waitlist channel for a moderator to approve
            msg = await suggestionWaitlistChannel.send(embed=sbaSuggestionEmbed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')

            try:
                # Waiting for a reaction response
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                if str(reaction) == '✅':
                    # If approved, send to the approved suggestions channel
                    await suggestionApproveChannel.send(embed=sbaSuggestionEmbed)
                    lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)
                    await lastMessage.add_reaction('✅')
                    await lastMessage.add_reaction('❌')

                    # Log approval
                    logEmbed = discord.Embed(title=f'SBA Suggestion was `Approved`', description=f'```{suggestion}```',
                                             color=0x00ff00, timestamp=datetime.utcnow())
                    logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                    logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                    signature(embedMessage=logEmbed)
                    await suggestionLogsChannel.send(embed=logEmbed)

                    # Delete suggestion from waitlist
                    await lastMessage.delete()
                elif str(reaction) == '❌':
                    # If rejected, delete message
                    lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)

                    # Log deletion
                    logEmbed = discord.Embed(title=f'SBA Suggestion was `Rejected`', description=f'```{suggestion}```',
                                             color=0xff0000, timestamp=datetime.utcnow())
                    logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                    logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                    signature(embedMessage=logEmbed)
                    await suggestionLogsChannel.send(embed=logEmbed)

                    # Delete suggestion from waitlist
                    await lastMessage.delete()
                else:
                    suggestionLogsChannel.send('Invalid Emoji')
            finally:
                pass
        # Suggestions for Discord
        elif sugtype == 'discord' or 'disc' or 'd':
            await ctx.message.add_reaction('✅')

            # Creates embedded message for suggestion
            discordSuggestionEmbed = discord.Embed(title=f'New Discord Suggestion by {ctx.message.author}',
                                                   description=f'```{suggestion}```', color=0x5865F2,
                                                   timestamp=datetime.utcnow())
            signature(embedMessage=discordSuggestionEmbed)
            discordSuggestionEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

            # Sends embed in the waitlist channel for a moderator to approve
            msg = await suggestionWaitlistChannel.send(embed=discordSuggestionEmbed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')

            try:
                # Waiting for a reaction response
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                if str(reaction) == '✅':
                    # If approved, send to the approved suggestions channel
                    await suggestionApproveChannel.send(embed=discordSuggestionEmbed)
                    lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)
                    await lastMessage.add_reaction('✅')
                    await lastMessage.add_reaction('❌')

                    # Log approval
                    logEmbed = discord.Embed(title=f'Discord Suggestion was `Approved`',
                                             description=f'```{suggestion}```',
                                             color=0x00ff00, timestamp=datetime.utcnow())
                    logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                    logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                    signature(embedMessage=logEmbed)
                    await suggestionLogsChannel.send(embed=logEmbed)

                    # Delete suggestion from waitlist
                    await lastMessage.delete()
                elif str(reaction) == '❌':
                    lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)

                    # Log deletion
                    logEmbed = discord.Embed(title=f'Discord Suggestion was `Rejected`',
                                             description=f'```{suggestion}```',
                                             color=0xff0000, timestamp=datetime.utcnow())
                    logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                    logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                    signature(embedMessage=logEmbed)
                    await suggestionLogsChannel.send(embed=logEmbed)

                    # Delete suggestion from waitlist
                    await lastMessage.delete()
                else:
                    suggestionLogsChannel.send('Invalid emoji')
            finally:
                pass
        elif sugtype is None:
            await ctx.message.add_reaction('❌')
            embed = discord.Embed(title='Error', description='Please enter `sba` or `discord` for your suggestion type',
                                  color=0xff0000, timestamp=datetime.utcnow())
            signature(embedMessage=embed)
            await ctx.send(embed=embed)

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ctx.message.author.mention} `{error}`')


def setup(bot):
    bot.add_cog(suggest(bot))
