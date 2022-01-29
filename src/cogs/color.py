import discord
from discord.ext import commands
from datetime import datetime


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
    )
    @commands.command()
    async def color(self, ctx, *, color=None):

        colors_PBT = [
            847438452400455680,  # Yellow PBT
            847438462382506044,  # Dark Green PBT
            847438463572639764,  # Lime Green PBT
            847438465444741150,  # Orange PBT
            847451392376963112,  # Red PBT
            847451397367922699,  # Dark Red PBT
            847451399838498906,  # Pink PBT
            847451402367926293,  # Light Pink PBT
            847451404720406528,  # Purple PBT
            847451407313403934,  # Turquoise PBT
            847451409921212426,  # Light Blue PBT
            847451412441858069,  # Blue PBT
            847451414913482763,  # Black PBT
            847451417651576832,  # Anti Light Mode PBT
            847451419740078091  # Anti Dark Mode PBT
        ]
        colors_TZT = [
            764967163806613525,  # Purple TZT
            764967159087890434,  # Blue TZT
            764967164431695932,  # Green TZT
            764967164611657739,  # Yellow TZT
            764967165320626217,  # Orange TZT
            764967191014539275,  # Red TZT
            850456245731065886  # Anti Dark Mode TZT
        ]
        colors_BB = [
            661730719340560385,  # Yellow BB
            661728230784499722,  # Dark Green BB
            661733723426914304,  # Lime Green BB
            661730659978444812,  # Orange BB
            661731297278033941,  # Light Red BB
            661731486394875907,  # Dark Red BB
            661731580007415808,  # Pink BB
            661731630913683466,  # Light Pink BB
            661731100355461120,  # Purple BB
            651552404059455507,  # Turquoise BB
            661732442779942912,  # Light Blue BB
            661730986572251167,  # Blue BB
            688430004530577430,  # Black BB
            662000476132343808,  # Anti Light Mode BB
            688430066514133074  # Anti Dark Mode BB
        ]
        user = ctx.message.author
        color = str(color)
        guild = ctx.guild.id

        # Clears all color roles from a user
        async def clear_color_roles():
            if guild == 815952235296063549:  # PBT
                for role_id in colors_PBT:
                    colorRole = discord.utils.get(ctx.guild.roles, id=role_id)
                    if colorRole in user.roles:
                        await user.remove_roles(colorRole)
            elif guild == 756305026627928175:  # TZT
                for role_id in colors_TZT:
                    colorRole = discord.utils.get(ctx.guild.roles, id=role_id)
                    if colorRole in user.roles:
                        await user.remove_roles(colorRole)
            elif guild == 450878205294018560:  # BB
                for role_id in colors_BB:
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
