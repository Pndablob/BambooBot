from datetime import datetime
import math
import time
import os
import logging

import discord
from discord.ext import commands

token = open("token.txt", "r").read()

bot = commands.Bot(command_prefix='p!', intents=discord.Intents().all())

# Start time (for `uptime` command)
startTime = round(time.time())
print(datetime.utcnow())


# 2ecc71 Hex code for color embeds
def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


@bot.event
async def on_connect():
    logging.info('Bot connected')


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
    logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')

    on_ready_channels = [
        820473911753310208
    ]

    # Sends a message in on_ready_channels stating the bot ready
    for on_ready_channels in on_ready_channels:
        ch = bot.get_channel(on_ready_channels)
        embed = discord.Embed(title='Bot Connected', color=0x08c744, timestamp=datetime.utcnow())
        signature(embedMessage=embed)
        await ch.send(embed=embed)


@bot.event
async def on_guild_available(guild):
    logging.info(f'Logged in {guild} ({guild.id})')

    # Checks if guild is BB
    if guild.id == 450878205294018560:
        # Loads all cogs on startup
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                logging.info(f'loaded {filename}')


@bot.command(aliases=['l'])
@commands.is_owner()
async def load(ctx, extension):
    msg = ctx.message

    if extension.lower() == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                    logging.info(f'loaded {filename}')
                except:
                    pass
        await ctx.send('Loaded all extensions')
        await msg.add_reaction('✅')
    else:
        try:
            bot.load_extension(f'cogs.{extension}')
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


@bot.command(aliases=['ut'])
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


# Verifies all users --> gives the 'Biscuit' role in BB
@bot.command(name='verifyall')
@commands.is_owner()
async def manuallyVerifyAll(ctx):
    role = discord.utils.get(ctx.guild.roles, id=472841496639307776)  # 'Biscuit' role
    msg = await ctx.send('Manually verifying all users...')
    i = 0

    for user in ctx.guild.members:
        if role not in user.roles:
            if len(msg.content) > 1950:
                await user.add_roles(role)
                msg = await ctx.send(f'\nVerified `{user}`')
            else:
                await user.add_roles(role)
                await msg.edit(content=msg.content + f'\nVerified `{user}`')

            i += 1
    await msg.edit(content=msg.content + f'\n\nDone! Manually verified `{i}` users')


# run bot
bot.run(token)
