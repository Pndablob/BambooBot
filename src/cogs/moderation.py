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

        global logging_ch
        logging_ch = self.bot.get_channel(879570002599084072)

    # Perm-Mute command
    @commands.command(name='permmute', aliases=['pmute'])
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        pass

    # Temp-Mute command
    @commands.command(name="tempmute", aliases=['tmute'])
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member: discord.Member, duration=None, *, reason=None):
        if not member:
            await ctx.send("Invalid member")
        elif reason is None:
            reason = "No Reason Provided"

        mutedRole = discord.utils.find(lambda r: r.name == "muted", ctx.guild.roles)
        await member.add_roles(mutedRole)

        await ctx.send(f"**{member}** was muted for `{duration}`. Reason: *{reason}*")

        muteEmbed = discord.Embed(description=f"**Reason:** {reason}", color=0xff0000, timestamp=datetime.utcnow())
        muteEmbed.set_author(name=f"{member} was muted for {duration}", icon_url=member.avatar_url)

        log = await logging_ch.send(embed=muteEmbed)

        memberDM = discord.Embed(description=f"You were muted in {ctx.guild} for {duration}", color=0x2ecc71, timestamp=datetime.utcnow())
        memberDM.add_field(name="Reason", value=f"{reason}")
        await member.send(embed=memberDM)

        await asyncio.sleep(timeToSeconds(duration))
        await member.remove_roles(mutedRole)

        unmuteEmbed = discord.Embed(description=f"**Reason:** {reason}", color=0x2ecc71)
        unmuteEmbed.add_field(name="Punishment Log Message", value=f"[Jump to punishment log message]({log.jump_url})")
        unmuteEmbed.set_author(name=f"{member} was unmuted", icon_url=member.avatar_url)
        await logging_ch.send(embed=unmuteEmbed)

    # Unmute command
    @commands.command(name='unmute')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        mutedRole = discord.utils.find(lambda r: r.name == "muted", ctx.guild.roles)

        if mutedRole not in member.roles:
            await ctx.send(f"{member} is not currently muted")
            return

        await member.remove_roles(mutedRole)

        await ctx.send(f"{member} was successfully unmuted. Reason: *{reason}*")

    # Perm-ban command
    @commands.command(name='permban', aliases=['pban'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if not member:
            await ctx.send("Invalid member")
        elif reason is None:
            reason = "Reason not provided"

        guild = ctx.guild
        await guild.ban(member, reason, delete_message_days=3)

        await ctx.send(f"**{member}** was permanently banned. Reason: *{reason}*")

        muteEmbed = discord.Embed(description=f"**Reason:** {reason}", color=0xff0000, timestamp=datetime.utcnow())
        muteEmbed.set_author(name=f"{member} was permanently banned", icon_url=member.avatar_url)

        log = await logging_ch.send(embed=muteEmbed)

        memberDM = discord.Embed(description=f"You were permanently banned in {ctx.guild}", color=0x2ecc71, timestamp=datetime.utcnow())
        memberDM.add_field(name="Reason", value=f"{reason}")
        await member.send(embed=memberDM)

    # Temp-ban command
    @commands.command(name='tempban', aliases=['tban'])
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, *, reason=None):
        pass

    # Unban command
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        pass


def setup(bot):
    bot.add_cog(moderation(bot))
