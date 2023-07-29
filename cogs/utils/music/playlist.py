import random
from collections import deque
from cogs.utils.music.config import *

from discord.ext import commands
import discord


class Playlist:
    """Stores a playlist of songs as youtube links"""

    def __init__(self):
        self.playlist = deque()
        self.history = deque()

        self.songname_history = deque()

        self.loop = False

    def __len__(self):
        return len(self.playlist)

    def add_name(self, name: str):
        self.songname_history.append(name)
        if len(self.playlist) > MAX_SONGNAME_HISTORY_LENGTH:
            self.songname_history.popleft()

    def add(self, track: str):
        self.playlist.append(track)

    def next(self, last_played):
        if self.loop:
            self.playlist.appendleft(self.history[-1])

        if len(self.playlist) == 0:
            return None

        if last_played != "filler":
            if len(self.history) > MAX_HISTORY_LENGTH:
                self.history.popleft()

        return self.playlist[0]

    def prev(self, current_song):
        if current_song is None:
            self.playlist.appendleft(self.history[-1])
            return self.playlist[0]

    def shuffle(self):
        random.shuffle(self.playlist)

    def move(self, old: int, new: int):
        temp = self.playlist[old]
        del self.playlist[old]
        self.playlist.insert(new, temp)

    def empty(self):
        self.playlist.clear()
        self.history.clear()
