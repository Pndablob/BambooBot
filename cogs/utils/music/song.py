from datetime import datetime, timedelta
from cogs.utils.constants import EMBED_COLOR

from discord.ext import commands
import discord


class Song:
    def __init__(self, filename, link: str = None, uploader: str = None, title: str = None, duration: int = None, channel_url: str = None, thumbnail: str = None):
        #self.info = self.SongInfo(song_url, uploader, title, duration, channel_url, thumbnail)

    #class SongInfo:
        #def __init__(self, song_url: str, uploader: str, title: str, duration: int, channel_url: str, thumbnail: str):
        self.filename = filename
        self.link = link
        self.uploader = uploader
        self.title = title
        self.duration = duration
        self.channel_url = channel_url
        self.thumbnail = thumbnail

    def format_embed(self) -> discord.Embed:
        """formats the song info into a discord embed"""
        embed = discord.Embed(title=f"Now playing", description=f"**[{self.title}]({self.link})**\nUploaded by **[{self.uploader}]({self.channel_url})**", color=EMBED_COLOR, timestamp=datetime.now())

        dur = str(timedelta(seconds=self.duration)) if self.duration is not None else "unknown"
        embed.add_field(name="Duration:", value=f"`{dur}`", inline=False)

        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)

        return embed
