import discord
from discord.ext import commands

from datetime import datetime


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


class seasonalRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Checks when a member has updated their nickname
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        role = discord.utils.find(lambda r: r.name == 'Spook', after.guild.roles)
        logging_channel = self.bot.get_channel(863854481773953055)

        if before.display_name != after.display_name:
            try:
                if after.display_name is None or "🎃" not in after.display_name:
                    await after.remove_roles(role)
                elif "🎃" in after.display_name:
                    await after.add_roles(role)

                embed = discord.Embed(title=f'Nickname Updated: ({after.id})', color=0x2ecc71,
                                      description=f'```md\n# {after.guild}```', timestamp=datetime.utcnow())
                embed.add_field(name='Nickname Before:', value=f'```{before.display_name}```', inline=False)
                embed.add_field(name='Nickname After:', value=f'```{after.display_name}```', inline=False)
                add_author(embed, after)

                await logging_channel.send(embed=embed)
            except:
                pass

    # Manually updates the seasonal role count
    @commands.command(name='updatedisplay', aliases=['ud'])
    @commands.is_owner()
    async def updateSeasonalRoleDisplay(self, ctx):
        display_channels = [
            862526927440707614,  # PBT
            863851458583592991,  # BB
        ]

        for channel in display_channels:
            try:
                ch = discord.utils.get(ctx.guild.voice_channels, id=channel)
                role = discord.utils.find(lambda r: r.name == 'Spook', ctx.guild.roles)

                await ch.edit(name=f'Spooky: {len(role.members)} 🎃')

                embed = discord.Embed(title=f'Display updated manually in guild `{ctx.guild}`', color=0x2ecc71,
                                      description=f'```{ch.name}```', timestamp=datetime.utcnow())
                signature(embed)

                await ctx.send(embed=embed)
                print(f'Display updated manually in {ctx.guild}')
            except AttributeError:
                pass

    # Gives all users with a 🎃 in nickname, the spooky role
    @commands.command(name='fixrole')
    @commands.is_owner()
    async def fixSeasonalRole(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=862837874365300766)  # sunny role
        msg = await ctx.send('Fixing seasonal role...')
        i = 0

        # Add roles
        for user in ctx.guild.members:
            if "🎃" in str(user.nick) and role not in user.roles:
                if len(msg.content) > 1950:
                    await user.add_roles(role)
                    msg = await ctx.send(f'\nAdded role to `{user}`')
                else:
                    await user.add_roles(role)
                    await msg.edit(content=msg.content + f'\nAdded role to `{user}`')

                i += 1
        await msg.edit(content=msg.content + f'\n\nDone! Added roles to `{i}` users')


def setup(bot):
    bot.add_cog(seasonalRoles(bot))
