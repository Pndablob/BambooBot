# TODO
# looping through playlist/song
# skipping song in queue
# shuffling play queue
# show next few songs in queue
# searching for song if not give a valid link

import logging
import os
import yt_dlp
from cogs.utils.music.config import *
from cogs.utils.music.playlist import Playlist
from cogs.utils.music.song import Song

import discord


log = logging.getLogger('discord')


class AudioController:
    """Controls audio playback"""

    def __init__(self, bot, interaction: discord.Interaction, volume: float):
        log.info("audio controller initialized")
        self.bot = bot

        self.channel = interaction.channel
        self.guild = interaction.guild

        self.queue = Playlist()

        self.now_playing = None
        self.volume = volume
        self.loop = False
        self.first = True
        # self.timer =

    def next_song(self, error):
        """Invoked after a song is finished. Plays the next song if there is one."""
        try:
            os.remove(f"{os.getcwd()}\\downloaded_audio.webm")
        except:
            pass

        self.now_playing = None

        print("Done playing song")
        print(f"playlist length {len(self.queue)}")

        next_song = self.queue.next()
        if next_song is None:
            if self.loop:
                next_song = self.queue.history.popleft()
            else:
                self.first = True
                print("Playlist empty")
                self.bot.loop.create_task(self.stop_player())
                return

        print(next_song.title)

        coro = self.play_song(next_song)
        self.bot.loop.create_task(coro)

    async def play_song(self, song: Song):
        """Plays a song object"""
        self.now_playing = song

        print(f"now playing: {self.now_playing.title}")

        try:
            self.guild.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.filename, options=FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.next_song(e))
            self.guild.voice_client.source.volume = self.volume
        except discord.ClientException as e:
            log.error(f"Error playing song: {e.__class__.__name__}")

    async def process_song(self, url, interaction: discord.Interaction = None):
        """Adds the track to the playlist instance and plays it, if it is the first song"""
        # ensure file is not downloaded
        try:
            os.remove(f"{os.getcwd()}\\downloaded_audio.webm")
        except:
            pass

        # attempt to pass through interaction
        #if interaction is None:
            #interaction = self.interaction

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
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
            data = ytdl.extract_info(url=url, download=True)
            filename = ytdl.prepare_filename(data)

        song = Song(filename=filename, link=url, uploader=data['uploader'], title=data['title'], duration=data['duration'], channel_url=data['channel_url'], thumbnail=data['thumbnail'])

        print(f"now processing {song.title}")

        self.queue.add(song)

        if self.now_playing is not None:
            embed = song.format_embed()
            embed.title = f"Added to queue `[{len(self.queue)}]`"
            await interaction.response.send_message(embed=embed)

            print(f"added {song.title} to queue")
            print(len(self.queue))
        elif self.now_playing is None:
            #track = url.split("&list=")[0]
            #await self.play_song(track)
            if self.first:
                self.first = False
                await interaction.response.send_message(embed=song.format_embed())
            else:
                await self.channel.send(embed=song.format_embed())

            await self.play_song(song)

    async def process_playlist(self, url):
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
            r = ytdl.extract_info(url, download=False)
            filename = ytdl.prepare_filename(r)

        for e in r['entries']:
            link = f"https://www.youtube.com/watch?v={e['id']}"

            song = Song(filename=filename, link=link, uploader=e['uploader'], title=e['title'], duration=e['duration'], channel_url=e['channel_url'], thumbnail=e['thumbnail'])

            self.queue.add(song)

        await self.process_song(self.queue.next())

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

