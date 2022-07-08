from datetime import datetime
import math
import time
import os
import logging

import discord
from discord.ext import commands


# 2ecc71 Hex code for color embeds
def signature(embed):
    # Signs embedded messages with a signature.
    embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


def main():
    @bot.event
    async def on_connect():
        logging.warning('Bot connected')

    @bot.event
    async def on_disconnect():
        logging.warning("Bot disconnected")
        ch = bot.get_channel(820473911753310208)

        await ch.send(f'```md\n# Bot disconnected```')

    @bot.event
    async def on_ready():
        # Removes 'help' command
        bot.help_command = None

        # When bot is ready, send ready message
        await bot.change_presence(activity=discord.Game('Bamboo Simulator'))
        logging.warning(f'Logged in as {bot.user.name} ({bot.user.id})')

        on_ready_channels = [
            820473911753310208
        ]

        # Sends a message in on_ready_channels stating the bot ready
        for on_ready_channels in on_ready_channels:
            ch = bot.get_channel(on_ready_channels)
            embed = discord.Embed(title='Bot Connected', color=0x08c744, timestamp=datetime.utcnow())
            signature(embed=embed)
            await ch.send(embed=embed)

    @bot.event
    async def on_guild_available(guild):
        logging.warning(f'Logged in {guild} ({guild.id})')

        # Checks if guild is BB
        if guild.id == 450878205294018560:
            # Loads all cogs on startup
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.load_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                    print(f'loaded {filename}')
            print(f"Bot startup time: {time.time()-startTime} seconds")

    @bot.command(aliases=['l'])
    @commands.is_owner()
    async def load(ctx, extension):
        msg = ctx.message

        if extension.lower() == 'all':
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        bot.load_extension(f'src.cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                        print(f'loaded {filename}')
                    except:
                        pass
            await ctx.send('Loaded all extensions')
            await msg.add_reaction('✅')
        else:
            try:
                bot.load_extension(f'src.cogs.{extension}')
                await ctx.send(f'Loaded `{extension}.py`')
                print(f'loaded {extension}.py')
                await msg.add_reaction('✅')
            except:
                await ctx.send("Extension already loaded or doesn't exist")
                await msg.add_reaction('❌')

    @bot.command(aliases=['ul'])
    @commands.is_owner()
    async def unload(ctx, extension):
        msg = ctx.message

        if extension.lower() == 'all':
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        bot.unload_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                        logging.warning(f'unloaded {filename}')
                    except:
                        pass
            await ctx.send('Unloaded all extensions')
            await msg.add_reaction('✅')
        else:
            try:
                bot.unload_extension(f'cogs.{extension}')
                await ctx.send(f'Unloaded `{extension}.py`')
                logging.warning(f'unloaded {extension}.py')
                await msg.add_reaction('✅')
            except:
                await ctx.send("Extension already unloaded or doesn't exist")
                await msg.add_reaction('❌')

    @bot.command(aliases=['rl'])
    @commands.is_owner()
    async def reload(ctx, extension):
        msg = ctx.message

        if extension.lower() == 'all':
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        bot.reload_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                        logging.warning(f'reloaded {filename}')
                    except:
                        pass
            await ctx.send('Reloaded all extensions')
            await msg.add_reaction('✅')
        else:
            try:
                bot.reload_extension(f'cogs.{extension}')
                await ctx.send(f'Reloaded `{extension}.py`')
                logging.warning(f'reloaded {extension}.py')
                await msg.add_reaction('✅')
            except:
                await ctx.send("Extension already reloaded or doesn't exist")
                await msg.add_reaction('❌')

    @bot.command(name='uptime', aliases=['ut'])
    @commands.is_owner()
    async def uptime(ctx):
        timediff = round(time.time() - startTime)  # Seconds since startup

        days = math.floor(timediff / 86400)  # Floor of diff / sec-in-day (86400)
        hours = math.floor((timediff % 86400) / 3600)  # Floor of (diff mod sec-in-day) / sec-in-hour (3600)
        minutes = math.floor((timediff % 3600) / 60)  # Floor of (diff mod sec-in-hour) / sec-in-min (60)
        seconds = (timediff % 60)  # diff mod sec-in-min

        embed = discord.Embed(title=f'<:online:876192917167964230> Uptime', color=0x2ecc71, timestamp=datetime.utcnow(),
                              description=f'`{days}` days, `{hours}` hours, `{minutes}` minutes, `{seconds}` seconds')
        signature(embed)

        await ctx.send(embed=embed)


if __name__ == '__main__':
    # init
    token = open("secrets.txt", "r").readlines()[0].rstrip()

    bot = commands.Bot(command_prefix=['p!', 'P!'], intents=discord.Intents().all())

    # Start time (for `uptime` command)
    startTime = round(time.time())
    logging.warning(datetime.utcnow())

    # main
    main()

    # run bot
    bot.run(token)
