import discord
from discord.ext import commands, tasks

from datetime import datetime
from src.bot import signature
from src.utils.enums import *


class timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not self.checkup.is_running():
            self.checkup.start()
        if not self.updateMemberCount.is_running():
            self.updateMemberCount.start()

    # Sends bot latency every 2 hours
    @tasks.loop(hours=2)
    async def checkup(self):
        ch = self.bot.get_channel(PBT.LOGS.value)
        embed = discord.Embed(title='Pong! 🏓', description=f'```{round(self.bot.latency * 1000)}ms```',
                              color=0x2ecc71, timestamp=datetime.utcnow())
        signature(embed)

        await ch.send(embed=embed)

    # Updates server member count display every hour
    @tasks.loop(minutes=60)
    async def updateMemberCount(self):
        guilds = [
            BB.ID.value,
        ]
        display_channels = [
            BB.MEMBER_DISPLAY.value,
        ]
        logging_channel = self.bot.get_channel(PBT.LOGS.value)

        for guild_id in guilds:
            guild = self.bot.get_guild(guild_id)
            index = guilds.index(guild_id)

            ch = discord.utils.get(guild.voice_channels, id=display_channels[index])

            await ch.edit(name=f'Members: {guild.member_count}')

            embed = discord.Embed(title=f'Member count updated in `{guild}`', color=0x2ecc71,
                                  description=f'```{ch.name}```', timestamp=datetime.utcnow())
            signature(embed)

            await logging_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(timers(bot))
