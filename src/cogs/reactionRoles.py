import discord
from discord.ext import commands

from datetime import datetime


class reactionRoles(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

        self.logChannel = self.bot.get_channel(820473911753310208)  # logging channel: #logs-seasonal-roles
        self.role_message_id = 989208667637288991  # ID of the message that can be reacted to add/remove a role.
        self.emoji_to_role = discord.PartialEmoji(animated=True, name='BambooBot', id=815952810297262181)  # ID of role

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)

            embed = discord.Embed(title="Member Verified", timestamp=datetime.utcnow(), color=0x00ff00)
            await self.logChannel.send(f"{payload.member.id}", embed=embed)
        except discord.HTTPException:
            await self.bot.get_channel(820473911753310208).send("<@317751950441447435> Reaction Role Error")


def setup(bot):
    bot.add_cog(reactionRoles(bot))
