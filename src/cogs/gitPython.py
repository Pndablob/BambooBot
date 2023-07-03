import discord
from discord.ext import commands

import git


class gitPython(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gitpull", aliases=["pull"])
    @commands.is_owner()
    async def pull(self, ctx, branch=None):
        if branch is None:
            branch = "master"

        git.cmd.Git().pull("https://github.com/Pndablob/BambooBot", branch)

        await ctx.send("Files updated successfully")


def setup(bot):
    bot.add_cog(gitPython(bot))
