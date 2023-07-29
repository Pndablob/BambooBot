from cogs.utils.constants import EMBED_COLOR

from discord.ext import commands
from discord import app_commands
import discord


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Bulk delete channel messages")
    @app_commands.describe(
        messages="number of messages"
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, messages: int):
        await interaction.channel.purge(limit=messages)
        await interaction.response.send_message(f"Purged **{messages}** messages in {interaction.channel.mention}", ephemeral=True)

    @app_commands.command(name='slowmode', description="Sets the channel slowmode")
    @app_commands.describe(
        seconds="slowmode delay"
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"Set the slowmode delay in {interaction.channel.mention} to `{seconds}` seconds", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Mod(bot))
