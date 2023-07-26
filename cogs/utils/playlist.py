import random
from collections import deque


class Playlist:
    """Stores a playlist of songs as youtube links"""

    def __init__(self):
        self.playlist = deque()

        self.loop = False

    def __len__(self):
        return len(self.playlist)

    def add(self, track: str):
        self.playlist.append(track)

    def next(self):
        pass
