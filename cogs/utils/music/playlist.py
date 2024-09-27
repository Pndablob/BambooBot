import random
from collections import deque

from discord.ext import commands
import discord


class Playlist:
    """Stores a playlist of Song objects"""

    def __init__(self):
        self.playlist = deque()
        self.history = deque()

        self.loop = False

    def __getitem__(self, item):
        return self.playlist[item]

    def __len__(self):
        return len(self.playlist)

    def add(self, song):
        self.playlist.append(song)

    def next(self):
        if self.loop:
            self.playlist.append(self.history.popleft())

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
        self.history.clear()
