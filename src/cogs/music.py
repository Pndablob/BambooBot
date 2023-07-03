import discord
from discord.ext import commands

import asyncio
import youtube_dl


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


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

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        ctx.voice_client.source.volume = volume / 100
        await ctx.message.reply(f"Changed volume to {volume}%")

    @commands.command()
    @commands.is_owner()
    async def stream(self, ctx, *, url=None):
        """Streams from an url but doesn't download"""

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        except discord.ClientException:
            pass

        await ctx.send(f'Now playing: **{player.title}**')

    @commands.command()
    async def play(self, ctx, *, url=None):
        """Add a song to the playlist and automatically play until the playlist is empty"""
        self.playlist.append(url)

        # If already playing song, only add it to the playlist

        while len(self.playlist) > 0:
            # Get the next song in the playlist
            url = self.playlist.pop(0)

            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            except discord.ClientException:
                await ctx.send("Error playing song")

            await ctx.send(f'Now playing: **{player.title}** `1/{len(self.playlist)+1}`')

    @commands.command()
    async def remove(self, ctx, index: int):
        # Remove the song from the playlist
        del self.playlist[index]
        await ctx.send('Song removed from playlist!')

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        """Pauses the bot from playing audio"""

        if ctx.voice_client.is_playing():
            await ctx.voice_client.pause()
            await ctx.message.reply("Paused audio")

    @commands.command()
    async def resume(self, ctx):
        """Resumes the paused audio"""

        if ctx.voice_client.is_paused():
            await ctx.voice_client.resume()
            await ctx.message.reply("Resumed audio")

    @stream.before_invoke
    @play.before_invoke
    @remove.before_invoke
    @volume.before_invoke
    @stop.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    async def ensure_voice(self, ctx):
        """Ensures user is connected to a voice channel upon invoking bot command"""

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.message.reply("You are not connected to a voice channel.")
                raise commands.CommandError("User not connected to a voice channel.")

"""
playlists = []

@client.command()
async def add(ctx, url: str):
    # Add the song to the playlist
    playlist.append(url)

    # Confirm that the song was added
    await ctx.send('Song added to playlist!')


@client.command()
async def remove(ctx, index: int):
    # Remove the song from the playlist
    del playlist[index]

    # Confirm that the song was removed
    await ctx.send('Song removed from playlist!')


@client.command()
async def play(ctx):
    voice_channel = ctx.message.author.voice.channel
    if voice_channel is not None:
        # Join the voice channel
        voice_client = await voice_channel.connect()

        # Keep playing songs until the playlist is empty
        while len(playlist) > 0:
            # Get the next song in the playlist
            url = playlist.pop(0)

            # Load the audio from the URL using FFmpeg
            audio_data = FFmpeg().load(url).to_data()

            # Play the audio using discord.opus
            try:
                voice_client.play(audio_data)
                await asyncio.sleep(audio_data.duration)
            except (OpusError, OpusNotLoaded, FFmpegError):
                # Handle any errors that may occur
                pass

        # Disconnect from the voice channel
        await voice_client.disconnect()
"""


def setup(bot):
    bot.add_cog(Music(bot))
