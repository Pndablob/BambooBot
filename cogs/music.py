import yt_dlp
import logging
from cogs.utils.music.audiocontroller import AudioController

from discord.ext import commands
from discord import app_commands
import discord

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

log = logging.getLogger('discord')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.controller = None

        self.controller_linked = False
        self.volume = 0.3

    def cog_unload(self) -> None:
        # self.bot.loop.create_task()
        pass

    def init_audio(self, interaction: discord.Interaction):
        self.controller = AudioController(bot=self.bot, interaction=interaction, volume=self.volume)

    @app_commands.command(name='play', description="Plays a song")
    @app_commands.describe(
        url="song link"
    )
    async def play(self, interaction: discord.Interaction, *, url: str):
        """
        Joins voice channel if not already
        Adds a song to the playlist and automatically plays until the playlist is empty
        """
        if not self.controller_linked:
            self.init_audio(interaction)
            self.controller_linked = True

        if interaction.guild.voice_client is None:
            await self.controller.connect_vc(interaction)

        await self.controller.process_song(url, interaction)
        # await interaction.response.send_message(embed=song.format_embed())

    """@app_commands.command(name='stream', description="Plays a song without downloading")
    @app_commands.describe(
        url="song link"
    )
    async def stream(self, interaction: discord.Interaction, *, url: str):
        # Joins voice channel if not already
        # Plays a song without downloading

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(channel)

        await channel.connect()

        try:
            player = await YTDLSource.from_url(url, loop=False, stream=True)
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        except discord.ClientException as e:
            await interaction.response.send_message(f"Error playing song: {e.__class__}", ephemeral=True)

        await interaction.response.send_message(f'Now playing: **{player.title}**')"""

    @app_commands.command(name='pause', description="Pauses the current audio or resumes paused audio")
    async def pause(self, interaction: discord.Interaction):
        """Pauses the bot from playing audio if already playing or resumes paused audio"""

        if interaction.guild.voice_client.is_playing() and interaction.guild.voice_client is not None:
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("Paused audio")
        elif interaction.guild.voice_client.is_paused() and interaction.guild.voice_client is not None:
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("Resumed audio")

    @app_commands.command(name='stop', description="Stops and disconnects the bot from voice")
    async def stop(self, interaction: discord.Interaction):
        """Stops and disconnects the bot from voice"""
        self.controller_linked = False

        await self.controller.disconnect_vc()

        await interaction.response.send_message(f"Stopped audio and disconnected bot from {interaction.user.voice.channel.mention}")

    @app_commands.command(name='volume', description="Changes the player's volume")
    async def volume(self, interaction: discord.Interaction, volume: app_commands.Range[int, 0, 100]):
        """Changes the player's volume"""
        interaction.guild.voice_client.source.volume = volume / 100
        self.controller.volume = volume
        await interaction.response.send_message(f"Changed volume to `{volume}`%")

    @app_commands.command(name='skip', description="Skips to the next song")
    async def skip(self, interaction: discord.Interaction):
        """Skips to the next song in the playlist"""
        interaction.guild.voice_client.stop()

    @app_commands.command(name='playlist', description="Shows the next 5 songs in the current playlist")
    async def show_playlist(self, interaction: discord.Interaction):
        """Returns the playlist of songs as a list of song titles"""
        await interaction.response.send_message(f"playlist: {str(self.controller.queue)}")

    @app_commands.command(name='playlist_shuffle', description="Shuffles the current playlist")
    async def playlist_shuffle(self, interaction: discord.Interaction):
        self.controller.queue.shuffle()

        await interaction.response.send_message(f"Shuffled playlist")

    @app_commands.command(name='playlist_loop', description="Loops the current playlist")
    async def playlist_loop(self, interaction: discord.Interaction):
        if self.controller.loop:
            self.controller.loop = False
            self.controller.queue.loop = False
            await interaction.response.send_message(f"Looping disabled")
        else:
            self.controller.loop = True
            self.controller.queue.loop = True
            await interaction.response.send_message(f"Looping enabled 🔁")

    @app_commands.command(name='playlist_clear', description="Clears the playlist")
    async def playlist_clear(self, interaction: discord.Interaction):
        self.controller.queue.empty()

        await interaction.response.send_message(f"Cleared the current playlist")


async def setup(bot):
    await bot.add_cog(Music(bot))
