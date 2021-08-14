from datetime import datetime

import discord
from discord.ext import commands
from discord.ext import tasks


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not self.checkup.is_running():
            self.checkup.start()

        if not self.updateDisplay.is_running():
            self.updateDisplay.start()

        if not self.updateMemberCount.is_running():
            self.updateMemberCount.start()

    # Sends bot latency ever 2 hours
    @tasks.loop(hours=2)
    async def checkup(self):
        ch = self.bot.get_channel(820473911753310208)
        embed = discord.Embed(title='Pong! 🏓', description=f'```{round(self.bot.latency * 1000)}ms```',
                              color=0x2ecc71, timestamp=datetime.utcnow())
        signature(embed)

        await ch.send(embed=embed)

    # Updates the seasonal-role display count every hour
    @tasks.loop(minutes=60)
    async def updateDisplay(self):
        guilds = [
            815952235296063549,  # PBT
            450878205294018560,  # BB
        ]
        display_channels = [
            862526927440707614,  # PBT
            863851458583592991,  # BB
        ]
        seasonal_role = [
            862520211142869053,  # PBT
            862837874365300766,  # BB
        ]
        logging_channel = self.bot.get_channel(863854481773953055)

        for guild_id in guilds:
            guild = self.bot.get_guild(id=guild_id)
            index = guilds.index(guild_id)

            ch = discord.utils.get(guild.voice_channels, id=display_channels[index])
            role = discord.utils.get(guild.roles, id=seasonal_role[index])

            await ch.edit(name=f'Sunny: {len(role.members)} 🌞')

            embed = discord.Embed(title=f'Display updated in guild `{guild}`', color=0x2ecc71,
                                  description=f'```{ch.name}```', timestamp=datetime.utcnow())
            signature(embed)

            await logging_channel.send(embed=embed)

    @tasks.loop(minutes=30)
    async def updateMemberCount(self):
        guilds = [
            450878205294018560,  # BB
        ]
        display_channels = [
            876187337174970418,  # BB
        ]
        logging_channel = self.bot.get_channel(863648426055041054)

        for guild_id in guilds:
            guild = self.bot.get_guild(id=guild_id)
            index = guilds.index(guild_id)

            ch = discord.utils.get(guild.voice_channels, id=display_channels[index])

            await ch.edit(name=f'Members: {guild.member_count}')

            embed = discord.Embed(title=f'Member count updated', color=0x2ecc71,
                                  description=f'```{ch.name}```', timestamp=datetime.utcnow())
            signature(embed)

            await logging_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(timers(bot))
