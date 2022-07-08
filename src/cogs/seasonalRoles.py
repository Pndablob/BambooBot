import discord
from discord.ext import commands, tasks

from datetime import datetime
from src.bot import signature


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


class seasonalRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not self.updateDisplay.is_running():
            self.updateDisplay.start()

        self.emoji = "🌞"
        self.roleName = "Sandy"
        self.BB = bot.get_guild(450878205294018560)  # BB
            
    # Updates the seasonal-role display count every hour
    @tasks.loop(minutes=60)
    async def updateDisplay(self):
        guilds = [
            815952235296063549,  # PBT
            450878205294018560,  # BB
        ]
        display_channels = [
            862526927440707614,  # PBT
            863851458583592991,  # BB
        ]
        seasonal_role = [
            862520211142869053,  # PBT
            862837874365300766,  # BB
        ]
        logging_channel = self.bot.get_channel(863854481773953055)

        for guild_id in guilds:
            guild = self.bot.get_guild(guild_id)
            index = guilds.index(guild_id)

            ch = discord.utils.get(guild.voice_channels, id=display_channels[index])
            role = discord.utils.get(guild.roles, id=seasonal_role[index])

            await ch.edit(name=f'{role.name}: {len(role.members)} {self.emoji}')

            embed = discord.Embed(title=f'Display updated in `{guild}`', color=0x2ecc71,
                                  description=f'```{ch.name}```', timestamp=datetime.utcnow())
            signature(embed)

            await logging_channel.send(embed=embed)

    # Checks when a member has updated their nickname
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        role = discord.utils.find(lambda r: r.name == self.roleName, after.guild.roles)
        logging_channel = self.bot.get_channel(863854481773953055)

        if before.display_name != after.display_name:
            try:
                if after.display_name is None or self.emoji not in after.display_name:
                    await after.remove_roles(role)
                elif self.emoji in after.display_name:
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
                role = discord.utils.find(lambda r: r.name == self.roleName, ctx.guild.roles)

                await ch.edit(name=f'{self.roleName}: {len(role.members)} {self.emoji}')

                embed = discord.Embed(title=f'Display updated manually in guild `{ctx.guild}`', color=0x2ecc71,
                                      description=f'```{ch.name}```', timestamp=datetime.utcnow())
                signature(embed)

                await ctx.send(embed=embed)
                print(f'Display updated manually in {ctx.guild}')
            except AttributeError:
                pass

    # Gives all users with an emoji in nick a seasonal role
    @commands.command(name='fixrole')
    @commands.is_owner()
    async def fixSeasonalRole(self, ctx):
        role = discord.utils.get(self.BB.roles, id=862837874365300766)  # Sandy role
        msg = await ctx.send('Fixing seasonal role...')
        i = 0

        # Add roles
        for user in self.BB.members:
            if self.emoji in str(user.nick) and role not in user.roles:
                if len(msg.content) > 1950:
                    await user.add_roles(role)
                    msg = await ctx.send(f'\nAdded role to `{user}`')
                else:
                    await user.add_roles(role)
                    await msg.edit(content=msg.content + f'\nAdded role to `{user}`')

                i += 1
        await msg.edit(content=msg.content + f'\n\nDone! Added roles to `{i}` users')

    # Clears all users with seasonal role
    @commands.command(name='cleanrole')
    @commands.is_owner()
    async def clearSeasonalRole(self, ctx):
        role = discord.utils.get(self.BB.roles, id=862837874365300766)  # Sandy role
        msg = await ctx.send('Fixing seasonal role...')
        i = 0

        # Add roles
        for user in self.BB.members:
            if self.emoji not in str(user.nick) and role in user.roles:
                if len(msg.content) > 1950:
                    await user.remove_roles(role)
                    msg = await ctx.send(f'\nRemoved role from `{user}`')
                else:
                    await user.remove_roles(role)
                    await msg.edit(content=msg.content + f'\nRemoved role from `{user}`')

                i += 1
        await msg.edit(content=msg.content + f'\n\nDone! Removed roles from `{i}` users')


def setup(bot):
    bot.add_cog(seasonalRoles(bot))
