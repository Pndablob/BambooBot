from discord.ext import commands
import discord


def add_author(embed: discord.Embed, author: discord.Member):
    # Signs embedded messages with a signature.
    embed.set_footer(text=f'{author.display_name}', icon_url=author.display_avatar.url)
