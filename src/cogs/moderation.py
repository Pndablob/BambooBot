import asyncio
from datetime import datetime

import discord
from discord.ext import commands


timeSuffix = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def timeToSeconds(time):
    try:
        return int(time[:-1]) * timeSuffix[time[-1]]
    except:
        return time


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, duration=None, *, reason=None):
        if not member:
            await ctx.send("Error")
        elif reason is None:
            reason = "No Reason Provided"

        mutedRole = discord.utils.find(lambda r: r.name == "muted", ctx.guild.roles)
        await member.add_roles(mutedRole)

        await ctx.send(f"**{member}** was muted for `{duration}`. Reason: *{reason}*")

        muteEmbed = discord.Embed(description=f"**Reason:** {reason}", color=0xff0000, timestamp=datetime.utcnow())
        muteEmbed.set_author(name=f"{member} was muted for {duration}", icon_url=member.avatar_url)

        logging_ch = self.bot.get_channel(879570002599084072)
        log = await logging_ch.send(embed=muteEmbed)

        memberDM = discord.Embed(description=f"You were muted in {ctx.guild} for {duration}", color=0x2ecc71, timestamp=datetime.utcnow())
        memberDM.add_field(name="Reason", value=f"{reason}")
        await member.send(embed=memberDM)

        if duration is not None:
            await asyncio.sleep(timeToSeconds(duration))
            await member.remove_roles(mutedRole)

            unmuteEmbed = discord.Embed(description=f"**Reason:** {reason}", color=0x2ecc71)
            unmuteEmbed.add_field(name="Punishment Log Message", value=f"[Jump to punishment log message]({log.jump_url})")
            unmuteEmbed.set_author(name=f"{member} was unmuted", icon_url=member.avatar_url)
            await logging_ch.send(embed=unmuteEmbed)


def setup(bot):
    bot.add_cog(moderation(bot))
