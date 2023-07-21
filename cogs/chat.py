from datetime import datetime

from discord.ext import commands
from discord import app_commands
import discord


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO send emojis/animated emojis on behalf of members
    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        """Sends animated emojis on behalf of members without nitro"""
        # Pass context
        ctx = await self.bot.get_context(message)

        if not isinstance(message.channel, discord.TextChannel) or message.author == self.bot.user.id:
            # Only in a text channel and message was not from bot
            return

        content = message.content

        if content.startswith(':') and content.endswith(':'):
            name = content[1:-1]

            try:
                for emoji in self.bot.emojis:
                    if emoji.name == name:
                        await ctx.send(emoji)
                        await message.delete()
            except:
                pass

    @commands.command(name='steal')
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def steal_emoji(self, ctx, emoji: discord.Emoji, *, name: str):
        """hippity hoppity your emoji is now my property"""
        pass

    @app_commands.command(name='echo', description="Echos a message")
    @app_commands.describe(
        message="The message to echo",
    )
    async def echo(self, interaction: discord.Interaction, *, message: str):
        """echos a message"""
        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Chat(bot))
