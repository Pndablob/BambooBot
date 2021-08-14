import discord
from discord.ext import commands

from datetime import datetime


class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """# When a member joins a guild
    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        ch = self.bot.get_channel(863648426055041054)  # '#Welcome' channel

        embed = discord.Embed(title=f'Welcome {member.name}', color=0x2ecc71, timestamp=datetime.utcnow(),
                              description=f"{member.mention}\n\n- Download SBA from <#472840465398628360>\n- Read our FAQ's in <#609442196055261221>"
                                          f"\n- Get SBA support in <#472840295097303040>\n- Grab some cool roles from <#603757944848384020>")
        embed.set_footer(text=f'ID: {member.id}', icon_url='https://cdn.discordapp.com/emojis/712401471504777247.gif?v=1')
        embed.set_thumbnail(url=member.avatar_url)

        await ch.send(embed=embed)"""


def setup(bot):
    bot.add_cog(welcome(bot))
