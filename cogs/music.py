import yt_dlp
import logging
from cogs.utils.music.config import *
from cogs.utils.music.audiocontroller import *

from discord.ext import commands
from discord import app_commands
import discord

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

log = logging.getLogger('discord')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.controller = None
        self.playlist = []

        self.controller_linked = False
        #self.volume = 0.5

    def cog_unload(self) -> None:
        # self.bot.loop.create_task()
        pass

    def init_audio(self, interaction: discord.Interaction):
        self.controller = AudioController(bot=self.bot, interaction=interaction, volume=self.volume)

    @app_commands.command(name='play', description="Plays a song")
    @app_commands.describe(
        url="song link"
    )
    async def play(self, interaction: discord.Interaction, *, url: str = "https://www.youtube.com/watch?v=9AFqO114Xq4"):
        """
        Joins voice channel if not already
        Adds a song to the playlist and automatically plays until the playlist is empty
        """
        log.info("play command invoked")

        if not self.controller_linked:
            self.init_audio(interaction)
            self.controller_linked = True

        if interaction.guild.voice_client is None:
            await self.controller.connect_vc(interaction=interaction)

        await self.controller.process_song(url)
        await interaction.response.send_message(f"now playing")

    """@app_commands.command(name='stream', description="Plays a song without downloading")
    @app_commands.describe(
        url="song link"
    )
    async def stream(self, interaction: discord.Interaction, *, url: str = "https://www.youtube.com/watch?v=9AFqO114Xq4"):
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

    @app_commands.command(name='pause', description="Pauses the current audio")
    async def pause(self, interaction: discord.Interaction):
        """Pauses the bot from playing audio"""

        if interaction.guild.voice_client.is_playing() and interaction.guild.voice_client is not None:
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("Paused audio")
        elif interaction.guild.voice_client.is_paused() and interaction.guild.voice_client is not None:
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("Resumed audio")

    @app_commands.command(name='join', description="Connects the bot to your voice channel")
    async def join(self, interaction: discord.Interaction):
        """Joins and connects to your voice channel"""

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(channel)

        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.mention} ")

    @app_commands.command(name='leave', description="Disconnects the bot from your current voice channel")
    async def leave(self, interaction: discord.Interaction):
        """Disconnects from your voice channel"""
        self.controller_linked = False

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.disconnect()

        await interaction.response.send_message(f"Left {channel.mention}")

    @app_commands.command(name='stop', description="Stops and disconnects the bot from voice")
    async def stop(self, interaction: discord.Interaction):
        """Stops and disconnects the bot from voice"""
        self.controller_linked = False

        if interaction.guild.voice_client is None:
            await interaction.response.send_message(f"Bot is already disconnected")

        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()

        if interaction.guild.voice_client.is_connected():
            await interaction.guild.voice_client.disconnect(force=True)

        await interaction.response.send_message("Stopped and disconnected bot")

    @app_commands.command(name='skip', description="Skips to the next song")
    async def skip(self, interaction: discord.Interaction):
        """Skips to the next song in the playlist"""
        #interaction.guild.voice_client.stop()

    @app_commands.command(name='volume', description="Changes the player's volume")
    async def volume(self, interaction: discord.Interaction, volume: app_commands.Range[int, 0, 100]):
        """Changes the player's volume"""
        interaction.guild.voice_client.source.volume = volume / 100
        #self.controller.volume = volume / 100
        await interaction.response.send_message(f"Changed volume to `{volume}`%")

    @app_commands.command(name='playlist', description="Views the current playlist")
    async def show_playlist(self, interaction: discord.Interaction):
        """Returns the playlist of songs as a list of song titles"""
        #await interaction.response.send_message(f"playlist: {self.controller.queue}")


async def setup(bot):
    await bot.add_cog(Music(bot))
