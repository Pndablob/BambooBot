import discord
from discord.ext import commands

from datetime import datetime
from src.utils.enums import *


class autoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.guild = self.bot.get_guild(Server.BB)  # BB
        self.logChannel = self.bot.get_channel(879570002599084072)  # logs-custom-bots
        self.role = self.guild.get_role(472841496639307776)  # get biscuit role

    # auto verify in BB for members older than 30 days
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if (datetime.now().timestamp() - member.created_at.timestamp()) > 2592000:
            await member.add_roles(self.role)

            embed = discord.Embed(title='Member Automatically Verified', description=f'Auto-verified <@{member.id}> (created: <t:{round(member.created_at.timestamp())}:R>)', color=0x00ff00)
        else:
            embed = discord.Embed(title='New Account Joined', description=f'<@{member.id}> (created: <t:{round(member.created_at.timestamp())}:R>)', color=0xff0000)
        await self.logChannel.send(f"{member.mention}", embed=embed)


def setup(bot):
    bot.add_cog(autoRole(bot))
