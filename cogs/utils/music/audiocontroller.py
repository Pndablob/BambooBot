# TODO:
#  looping through playlist/song --> needs refining
#  bug with volume cmd when looping
#  skipping song in queue
#  shuffling play queue
#  show next few songs in queue
#  searching for song if not give a valid link

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

    def next_song(self, error):
        """Invoked after a song is finished. Plays the next song if there is one."""
        try:
            os.remove(f"{os.getcwd()}\\{FILENAME}")
        except:
            pass

        self.now_playing = None

        print("Done playing song")
        print(f"playlist length {len(self.queue)}")

        """if len(self.queue) == 0:
            if self.loop:
                self.queue.history.appendleft(self.queue[0])
                next_song = self.queue.history.popleft()
            else:
                self.first = True
                print("Playlist empty")
                self.bot.loop.create_task(self.stop_player())
                return
        else:
            next_song = self.queue.next()"""

        next_song = self.queue.next()
        if next_song is None:
            self.first = True
            print("Playlist empty")
            self.bot.loop.create_task(self.stop_player())
            return

        print(next_song.title)

        self.bot.loop.create_task(self.process_song(next_song.link))

    async def play_song(self, song: Song):
        """Plays a song object"""
        self.now_playing = song

        self.queue.history.append(self.now_playing)

        self.queue.playlist.popleft()

        try:
            print(f"now playing: {self.now_playing.title}")
            self.guild.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(FILENAME, options=FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.next_song(e))
            self.guild.voice_client.source.volume = self.volume
            print(f"changed volume to {self.volume}")
        except discord.ClientException as e:
            log.error(f"Error playing song: {e.__class__.__name__}")

    async def process_song(self, url: str, interaction: discord.Interaction = None):
        """Adds the track to the playlist instance and plays it, if it is the first song"""
        # ensure file is not downloaded
        try:
            os.remove(f"{os.getcwd()}\\{FILENAME}")
        except:
            pass

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

        song = Song(link=url, uploader=data['uploader'], title=data['title'], duration=data['duration'], channel_url=data['channel_url'], thumbnail=data['thumbnail'])

        print(f"now processing {song.title}")
        self.queue.add(song)
        print(f"adding {song.title} to queue")

        if self.now_playing is not None:
            embed = song.format_embed()
            embed.title = f"Added to queue `[{len(self.queue)}]`"
            await interaction.response.send_message(embed=embed)

            print(f"added {song.title} to queue")
            print(len(self.queue))
        else:
            if self.first:
                self.first = False
                await interaction.response.send_message(embed=song.format_embed())
            else:
                await self.channel.send(embed=song.format_embed())

            await self.play_song(self.queue.playlist[0])

    async def process_playlist(self, url):
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
            r = ytdl.extract_info(url, download=False)

        for e in r['entries']:
            link = f"https://www.youtube.com/watch?v={e['id']}"

            song = Song(link=link, uploader=e['uploader'], title=e['title'], duration=e['duration'], channel_url=e['channel_url'], thumbnail=e['thumbnail'])

            self.queue.add(song)
            print(f"adding {song.title} to queue")

        await self.process_song(self.queue.next().link)

    async def stop_player(self):
        """stops the player"""
        # ignores if voice client not found or already is stopped
        if self.guild.voice_client is None or (not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return

        self.now_playing = None
        self.queue.loop = False
        self.guild.voice_client.stop()

    async def connect_vc(self, interaction: discord.Interaction):
        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(channel)

        if not interaction.user.voice:
            await interaction.response.send_message("Please join a voice channel")
            return

        if self.guild.voice_client is None:
            await channel.connect(reconnect=True)
        else:
            await interaction.response.send_message("Already connected to a voice channel")

    async def disconnect_vc(self):
        await self.stop_player()
        await self.guild.voice_client.disconnect(force=True)

