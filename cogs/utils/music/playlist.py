import random
from collections import deque
from cogs.utils.music.config import *
from cogs.utils.music.song import Song

from discord.ext import commands
import discord


class Playlist:
    """Stores a playlist of Song objects"""

    def __init__(self):
        self.playlist = deque()

    def __len__(self):
        return len(self.playlist)

    def add(self, song):
        self.playlist.append(song)

    def next(self, last_played=None):
        try:
            next_song = self.playlist.popleft()
        except IndexError:
            return None

        return next_song

    def shuffle(self):
        random.shuffle(self.playlist)

    def move(self, old: int, new: int):
        temp = self.playlist[old]
        del self.playlist[old]
        self.playlist.insert(new, temp)

    def empty(self):
        self.playlist.clear()
