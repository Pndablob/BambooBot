import discord
from discord.ext import commands

from datetime import datetime
from src.utils.enums import *


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


class colorRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role(
        # Guild: PBT
        815952833253605426,  # *
        835998900846198795,  # Bot
        # Guild: BB
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
        638208291469656103,  # Small Creator
        620718100320354316,  # Contributor
        726301638679199744,  # 15m Giveaway
        798764137936977952,  # New Biscuit (Level 10)
        # Guild: TZT
        845089203788578857,  # nerd
        891424837719978034,  # people
    )
    @commands.command()
    async def color(self, ctx, *, color=None):
        user = ctx.message.author
        color = str(color)
        guild = ctx.guild.id

        # Clears all color roles from a user
        async def clear_color_roles():
            if guild == PBT.ID.value:
                for role_id in PBT.COLORS.value:
                    colorRole = discord.utils.get(ctx.guild.roles, id=role_id)
                    if colorRole in user.roles:
                        await user.remove_roles(colorRole)
            elif guild == TZT.ID.value:
                for role_id in TZT.COLORS.value:
                    colorRole = discord.utils.get(ctx.guild.roles, id=role_id)
                    if colorRole in user.roles:
                        await user.remove_roles(colorRole)
            elif guild == BB.ID.value:
                for role_id in BB.COLORS.value:
                    colorRole = discord.utils.get(ctx.guild.roles, id=role_id)
                    if colorRole in user.roles:
                        await user.remove_roles(colorRole)

        if color.title() == 'Clear' or color.title() == 'Remove' or color.title() == 'None':
            await clear_color_roles()

            embed = discord.Embed(title='Color Roles Cleared', description=f'Your color roles have been removed',
                                  color=0xffffff, timestamp=datetime.utcnow())
            add_author(embedMessage=embed, author=ctx.author)
            await ctx.send(embed=embed)
        else:
            await clear_color_roles()

            role = discord.utils.find(lambda r: r.name == f'Color - {color.title()}', ctx.guild.roles)
            await user.add_roles(role)
            embed = discord.Embed(title='Color Role Given', description=f'Your color is now: `{color.title()}`',
                                  color=role.color, timestamp=datetime.utcnow())
            add_author(embedMessage=embed, author=ctx.author)
            await ctx.send(embed=embed)

    @color.error
    async def _color_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(title='Insignificant Permission', color=0xff0000, timestamp=datetime.utcnow(),
                                  description='You lack a required role to use this command.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention}, Please enter the required arguments')
        else:
            raise error


def setup(bot):
    bot.add_cog(colorRoles(bot))
