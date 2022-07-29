from discord.ext import commands
import discord

from src.utils.enums import *


class biscuitbakery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Verifies all users --> gives the 'Biscuit' role in BB
    @commands.command(name="verifyall")
    @commands.is_owner()
    async def verifyAlll(self, ctx):
        guild = self.bot.get_guild(Server.BB)  # BB
        role = guild.get_role(role_id=472841496639307776)  # 'Biscuit' role
        msg = await ctx.send('Manually verifying all users...')
        i = 0

        for user in guild.members:
            if role not in user.roles:
                if len(msg.content) > 1950:
                    await user.add_roles(role)
                    msg = await ctx.send(f'\nVerified `{user}`')
                else:
                    await user.add_roles(role)
                    await msg.edit(content=msg.content + f'\nVerified `{user}`')

                i += 1
        await msg.edit(content=msg.content + f'\n\nDone! Manually verified `{i}` users')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def verify(self, ctx, user: discord.Member):
        if ctx.guild == Server.BB or ctx.guild == Server.PBT:
            guild = self.bot.get_guild(Server.BB)
        else:
            # if not BB
            return

        role = guild.get_role(472841496639307776)  # biscuit role
        member = guild.get_member(user)  # get member in BB

        try:
            await member.add_roles(role)
            await ctx.send(f"Successfully verified {member.mention}")
        except:
            await ctx.send(f"Verification failed for whatever reason")


def setup(bot):
    bot.add_cog(biscuitbakery(bot))
