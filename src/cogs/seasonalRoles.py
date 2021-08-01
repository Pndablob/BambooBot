import discord
from discord.ext import commands
from datetime import datetime


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


class seasonalRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Checks when a member has updated their nickname
    @commands.Cog.listener()
    @commands.has_any_role(
        # BB
        653624748311576632,  # Staff
        578281324914278410,  # Collaborator
        617803927240310823,  # Ebic Translator
        733448745517187134,  # Patron
        614357920351649805,  # Nitro Booster
        673728339076317184,  # Epic Coders
        623288545439645706,  # Partners
        646106899737083945,  # Hypixel Staffy People
        603719761934942238,  # Creator
        472841524804190208,  # Friend
        726301638679199744,  # Giveaway 15m
        517488615694008321,  # Cool Green Role
        798764352823623720,  # Level 50
    )
    async def on_member_update(self, before, after):

        role = discord.utils.find(lambda r: r.name == 'Sunny 🌞', after.guild.roles)
        logging_channel = self.bot.get_channel(863854481773953055)

        if before.display_name != after.display_name:
            try:
                if after.display_name is None or "🌞" not in after.display_name:
                    await after.remove_roles(role)
                elif "🌞" in after.display_name:
                    await after.add_roles(role)

                embed = discord.Embed(title=f'Nickname Updated: {after.name} ({after.id})', color=0x2ecc71,
                                      description=f'```md\n# {after.guild}```', timestamp=datetime.utcnow())
                embed.add_field(name='Nickname Before:', value=f'```{before.display_name}```', inline=False)
                embed.add_field(name='Nickname After:', value=f'```{after.display_name}```', inline=False)
                add_author(embed, after)

                await logging_channel.send(embed=embed)
            except:
                pass


def setup(bot):
    bot.add_cog(seasonalRoles(bot))
