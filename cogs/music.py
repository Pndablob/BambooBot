import asyncio
import yt_dlp

from discord.ext import commands
from discord import app_commands
import discord

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }

ffmpeg_options = {
        'options': '-vn',
    }

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.playlist = []

    @app_commands.command(name='join', description="Connects the bot to your voice channel")
    async def join(self, interaction: discord.Interaction):
        """Joins and connects to your voice channel"""
        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(channel)

        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.mention} ", ephemeral=True)

    @app_commands.command(name='leave', description="Disconnects the bot from your current voice channel")
    async def leave(self, interaction: discord.Interaction):
        """Disconnects from your voice channel"""
        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.disconnect()

        await interaction.response.send_message(f"Left {channel.mention}", ephemeral=True)

    @app_commands.command(name='play', description="Plays a song")
    @app_commands.describe(
        url="song link"
    )
    async def play(self, interaction: discord.Interaction, *, url: str):
        """
        Joins voice channel if not already
        Adds a song to the playlist and automatically plays until the playlist is empty
        """
        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(channel)

        await channel.connect()

        try:
            player = await YTDLSource.from_url(url, loop=False, stream=True)
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        except discord.ClientException:
            await interaction.response.send_message("Error playing song", ephemeral=True)

        await interaction.response.send_message(f'Now playing: **{player.title}** `[1/{len(self.playlist) + 1}]`')

    @app_commands.command(name='pause', description="Pauses the current audio")
    async def pause(self, interaction: discord.Interaction):
        """Pauses the bot from playing audio"""
        if interaction.guild.voice_client.is_playing() and interaction.guild.voice_client is not None:
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("Paused audio", ephemeral=True)

    @app_commands.command(name='resume', description="Resumes the paused audio")
    async def resume(self, interaction: discord.Interaction):
        """Resumes the paused audio"""
        if interaction.guild.voice_client.is_paused() and interaction.guild.voice_client is not None:
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("Resumed audio", ephemeral=True)

    @app_commands.command(name='stop', description="Stops and disconnects the bot from voice")
    async def stop(self, interaction: discord.Interaction):
        """Stops and disconnects the bot from voice"""
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()

        if interaction.guild.voice_client.is_connected():
            await interaction.guild.voice_client.disconnect(force=False)

        await interaction.response.send_message("Stopped and disconnected bot", ephemeral=True)

    @app_commands.command(name='skip', description="Skips to the next song")
    async def next(self, interaction: discord.Interaction):
        """Skips to the next song in the playlist"""
        pass

    @app_commands.command(name='volume', description="Changes the player's volume")
    @app_commands.describe(
        vol="volume"
    )
    async def volume(self, interaction: discord.Interaction, vol: app_commands.Range[int, 0, 100]):
        """Changes the player's volume"""
        interaction.guild.voice_client.source.volume = vol / 100
        await interaction.response.send_message(f"Changed volume to `{vol}`%")

    @app_commands.command(name='add', description="Adds a song to the playlist")
    async def add_track(self, interaction: discord.Interaction):
        """Appends a song to the end of the current playlist"""
        pass

    @app_commands.command(name='playlist', description="Views the current playlist")
    async def show_playlist(self, interaction: discord.Interaction):
        """Returns the playlist of songs as a list of song titles"""
        pass




async def setup(bot):
    await bot.add_cog(Music(bot))
