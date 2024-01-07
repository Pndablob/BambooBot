import asyncio
import logging
import os
import yt_dlp
from cogs.utils.music.config import *
from cogs.utils.music.playlist import Playlist
from cogs.utils.music.song import Song

import discord


log = logging.getLogger('discord')

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        #print(data)

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

    def __init__(self, bot, interaction: discord.Interaction, volume: float):
        log.info("audio controller initialized")
        self.bot = bot

        self.interaction = interaction
        self.guild = interaction.guild

        self.queue = Playlist()
        #self.queue.add("https://www.youtube.com/watch?v=9AFqO114Xq4")
        #self.queue.add("https://www.youtube.com/watch?v=ciwx8yJPX54")
        #self.queue.add("https://www.youtube.com/watch?v=HzdD8kbDzZA")

        self.now_playing = None
        self.volume = volume
        # self.timer =

    def next_song(self, error):
        """Invoked after a song is finished. Plays the next song if there is one."""
        os.remove(f"{os.getcwd()}\\downloaded_audio.webm")
        print("Done playing song")
        print(f"playlist length {len(self.queue)}")

        next_song = self.queue.next(self.now_playing)

        print(next_song.title)

        self.now_playing = None

        if next_song is None:
            print("Playlist empty")
            self.bot.loop.create_task(self.stop_player())
            return

        # await self.play_song(next_song)

        # asyncio.get_event_loop().run_until_complete(self.play_song(next_song))

        coro = self.play_song(next_song)
        self.bot.loop.create_task(coro)

    async def play_song(self, song: Song):
        """Plays a song object"""
        self.now_playing = song

        await self.interaction.channel.send(embed=song.format_embed())

        print(f"now playing: {self.now_playing.title}")

        try:
            player = await YTDLSource.from_url(song.link, loop=False, stream=False)
            self.guild.voice_client.play(player, after=lambda e: self.next_song(e))
            self.guild.voice_client.source.volume = self.volume
        except discord.ClientException as e:
            log.error(f"Error playing song: {e.__class__.__name__}")

    async def process_song(self, url, interaction: discord.Interaction = None):
        """Adds the track to the playlist instance and plays it, if it is the first song"""
        # attempt to pass through interaction
        if interaction is None:
            interaction = self.interaction

        # check if is valid youtube url
        is_url = True if ("https://www.youtu" in url or "https://youtu.be" in url) else False
        if not is_url:
            await interaction.channel.send(f"Invalid Youtube link")
            # search youtube
            return

        # Check whether to process as playlist
        is_playlist = True if "playlist?list=" in url else False
        if is_playlist:
            # process playlist
            await self.process_playlist(url)
            return

        # extract info from url to Song object
        info = ytdl.extract_info(url=url, download=False)

        song = Song(link=url, uploader=info['uploader'], title=info['title'], duration=info['duration'], channel_url=info['channel_url'], thumbnail=info['thumbnail'])

        print(f"now processing {song.title}")
        try:
            os.remove(f"{os.getcwd()}\\downloaded_audio.webm")
        except:
            pass

        if self.now_playing is not None:
            self.queue.add(song)

            embed = song.format_embed()
            embed.title = f"Added to queue `[{len(self.queue)}]`"
            await interaction.response.send_message(embed=embed)

            print(f"added {song.title} to queue")
            print(len(self.queue))
        elif self.now_playing is None:
            #track = url.split("&list=")[0]
            #await self.play_song(track)
            await self.play_song(song)

    async def process_playlist(self, url):
        r = ytdl.extract_info(url, download=False)

        for e in r['entries']:
            link = f"https://www.youtube.com/watch?v={e['id']}"

            song = Song(link=link, uploader=e['uploader'], title=e['title'], duration=e['duration'], channel_url=e['channel_url'], thumbnail=e['thumbnail'])

            self.queue.add(song)

        await self.play_song(self.queue.next())

    async def stop_player(self):
        """stops the player"""

        # ignores if voice client not found or already is stopped
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return

        self.now_playing = None
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

