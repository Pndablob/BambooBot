import asyncio
import logging
import os
import yt_dlp
from cogs.utils.music.playlist import Playlist
from cogs.utils.music.config import *

import discord


log = logging.getLogger('discord')

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


class AudioController(object):
    """Controls audio playback"""

    def __init__(self, bot, interaction: discord.Interaction):
        self.bot = bot

        self.interaction = interaction
        self.guild = interaction.guild

        self.queue = Playlist()

        self.now_playing = None
        # self.timer =

    def next_song(self, error):
        """Invoked after a song is finished. Plays the next song if there is one."""
        if self.guild.voice_client.is_playing():
            self.guild.voice_client.stop()

        os.remove(f"{os.getcwd()}\\downloaded_audio.webm")

        print("Done playing song")
        return

    async def play_song(self, song):
        """Plays a song object"""
        try:
            player = await YTDLSource.from_url(song, loop=False, stream=False)
            self.guild.voice_client.play(player, after=lambda e: self.next_song(e))
        except discord.ClientException as e:
            log.error(f"Error playing song: {e.__class__.__name__}")

    async def process_song(self, track):
        """Adds the track to the playlist instance and plays it, if it is the first song"""

        # check if is valid youtube url
        is_url = True if ("https://www.youtu" in track or "https://youtu.be" in track) else False
        is_playlist = True if "playlist?list=" in track else False

        if not is_url:
            await self.interaction.response.send_message(f"Invalid Youtube link")
            return

        if is_playlist:
            await self.process_playlist(track)

            if self.now_playing is None:
                await self.play_song(self.queue.playlist[0])

        track = track.split("&list=")[0]

    async def process_playlist(self, track):
        pass

    async def stop_player(self):
        """stops the player"""

        # ignores if voice client not found or already is stopped
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return

        self.queue.loop = False
        self.guild.voice_client.stop()

    async def register_voice_channel(self, channel: discord.VoiceChannel):
        await channel.connect(reconnect=True)

    async def connect_vc(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("Please join a voice channel")

        if self.guild.voice_client is None:
            await self.register_voice_channel(interaction.user.voice.channel)
        else:
            await interaction.response.send_message("Already connected to a voice channel")

    async def disconnect_vc(self):
        await self.stop_player()
        await self.guild.voice_client.disconnect(force=True)

