from datetime import datetime
from cogs.utils.constants import EMBED_COLOR

from discord.ext import commands
from discord import app_commands
import discord
import requests


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user", description="Shows information about a user")
    @app_commands.describe(
        member="The member to show info about",
    )
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        """shows information about a user"""
        if member is None:
            member = interaction.user

        fields = [
            ('Mention', member.mention, False),
            ('Create Date', f'<t:{round(member.created_at.timestamp())}:f>', False),
            ('Join Date', f'<t:{round(member.joined_at.timestamp())}:f>', False)
        ]
        role_list = ""
        badge_list = ""

        # add badges
        if member == interaction.guild.owner:
            badge_list += "<:ServerOwner:1128899832921215017> "
        for f in member.public_flags.all():
            match f.value:
                case 1:
                    badge_list += "<:DiscordStaff:1128899787996016761> "  # staff
                case 2:
                    badge_list += "<:Partner:1128899786523803798> "  # partner
                case 4:
                    badge_list += "<:HypesquadEvents:1128899785403928576> "  # hypesquad events
                case 8:
                    badge_list += "<:BugHunter:1128899875078152232> "  # bug_hunter
                case 64:
                    badge_list += "<:HypesquadBravery:1128899830404616213> "  # hypesquad bravery
                case 128:
                    badge_list += "<:HypesquadBrilliance:1128899831922970797> "  # hypesquad brilliance
                case 256:
                    badge_list += "<:HypesquadBalance:1128899829477670933> "  # hypesquad balance
                case 512:
                    badge_list += "<:EarlySupporter:1128899788457394227 "  # early supporter
                case 16384:
                    badge_list += "<:BugHunter2:1128899873891176488> "  # bug hunter level 2
                case 131072:
                    badge_list += "<:VerifiedDeveloper:1128899793356328980> "  # verified bot developer
                case 262144:
                    badge_list += "<:CertifiedMod:1128899784317599744> "  # discord moderator academy alumni
                case 4194304:
                    badge_list += "<:ActiveDeveloper:1128906229880733718> "  # active developer

        color = EMBED_COLOR if len(member.roles) == 1 else member.color

        embed = discord.Embed(title=f"{member.name}", color=color, timestamp=datetime.now(),
                              description=badge_list[:-1])
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=member.id)

        # add fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # add roles
        for roles in reversed(member.roles[1:]):
            role_list += f"{roles.mention}, "
        embed.add_field(name=f'Roles [{len(member.roles) - 1}]', value=role_list[:-2])

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="server", description="Shows information about the current server")
    async def guild_info(self, interaction: discord.Interaction):
        """shows information about the current guild"""
        guild = interaction.guild

        fields = [
            ("Members", f"<:members:1128921808171716688> {guild.member_count}", False),
            ("Channels", f"**Total:** {len(guild.channels) - len(guild.categories)}\n<:TextChannels:1128899782778310736> {len(guild.text_channels)}\n<:VoiceChannels:1128899781612277761> {len(guild.voice_channels)}", False)
        ]
        role_list = ""

        color = EMBED_COLOR if len(guild.owner.roles) == 1 else guild.owner.color

        embed = discord.Embed(description=f"Created by **{guild.owner.name}** <t:{round(guild.created_at.timestamp())}:R>",
                              color=color, timestamp=datetime.now())
        embed.set_author(name=guild.name, url=guild.icon.url)
        embed.set_footer(text=guild.id)

        # add fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # add roles
        for roles in reversed(guild.roles[1:]):
            if len(role_list) >= 1000:
                role_list += f"... and more!"
                break
            role_list += f"{roles.mention}, "

        embed.add_field(name=f'Roles [{len(guild.roles) - 1}]', value=role_list[:-2])

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='mcserver', description="Shows information about a Minecraft server")
    @app_commands.describe(
        server="The server to show info about",
    )
    async def mcserver_info(self, interaction: discord.Interaction, server: str):
        """shows information about a Minecraft server"""
        response = requests.get(f"https://api.mcsrvstat.us/3/{server}")
        data = response.json()

        if data['online']:
            embed = discord.Embed(title="Server Status <:online:1127821209921400833>", color=EMBED_COLOR, timestamp=datetime.now(),
                                  description=
                                  f"**IP:** `{data['ip']}`\n"
                                  f"**Version:** `{data['version']}`\n"
                                  f"**MOTD:** `{data['motd']['clean'][0]}`\n"
                                  f"**Players:** `{data['players']['online']}/{data['players']['max']}`"
                                  )
            embed.set_thumbnail(url=f"https://eu.mc-api.net/v3/server/favicon/{server}")

            player_list = []
            for player in data['players']['list']:
                player_list.append(player['name'])
            if len(player_list) > 0:
                embed.add_field(name=f"Players [{len(player_list)}]", value=f"```{', '.join(player_list)}```", inline=False)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Server `{server}` is offline")

    # TODO bot info command
    @app_commands.command(name="about", description="Shows information about the bot")
    async def server_info(self, interaction: discord.Interaction):
        """shows information about the bot"""
        embed = discord.Embed()
        embed.set_author(name="Bamboo Bot", icon_url="https://cdn.discordapp.com/emojis/851191181315538965.webp?size=128&quality=lossless")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
