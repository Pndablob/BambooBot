from datetime import datetime
import contextlib
import io

import discord
from discord.ext import commands


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


class _eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eval', aliases=['ev'])
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        str_obj = io.StringIO()  # Retrieves a stream of data

        cleaned_code = clean_code(code)  # Removing code block segments

        if code.startswith('```py'):
            try:
                with contextlib.redirect_stdout(str_obj):
                    exec(cleaned_code)
            except Exception as e:
                result = f'{e.__class__.__name__}: {e}'

                ev_embed = discord.Embed(title=f'Eval Failed', color=0xff0000, timestamp=datetime.utcnow())
                ev_embed.add_field(name=f'📥 Input', value=f'```{cleaned_code}```', inline=False)
                ev_embed.add_field(name=f'📤 Result', value=f'```{result}```', inline=False)
                signature(ev_embed)

                await ctx.send(embed=ev_embed)
            else:
                result = f'{str_obj.getvalue()}'

                ev_embed = discord.Embed(title=f'Eval Successful', color=0x00ff00, timestamp=datetime.utcnow())
                ev_embed.add_field(name=f'📥 Input', value=f'```{cleaned_code}```', inline=False)
                ev_embed.add_field(name=f'📤 Result', value=f'```{result}```', inline=False)
                signature(ev_embed)

                await ctx.send(embed=ev_embed)
        else:
            local_variables = {
                "discord": discord,
                "commands": commands,
                "bot": self.bot,
                "ctx": ctx,
                "channel": ctx.channel,
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message
            }

            try:
                result = eval(code, local_variables)
            except Exception as e:
                result = f"{e.__class__.__name__}: {e}"

                ev_embed = discord.Embed(title=f'Eval Failed', color=0xff0000, timestamp=datetime.utcnow())
                ev_embed.add_field(name=f'📥 Input', value=f'```{cleaned_code}```', inline=False)
                ev_embed.add_field(name=f'📤 Result', value=f'```{result}```', inline=False)
                signature(ev_embed)

                await ctx.send(embed=ev_embed)
            else:
                ev_embed = discord.Embed(title=f'Eval Successful', color=0x00ff00, timestamp=datetime.utcnow())
                ev_embed.add_field(name=f'📥 Input', value=f'```{cleaned_code}```', inline=False)
                ev_embed.add_field(name=f'📤 Result', value=f'```{result}```', inline=False)
                signature(ev_embed)

                await ctx.send(embed=ev_embed)


def setup(bot):
    bot.add_cog(_eval(bot))
