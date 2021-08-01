from datetime import datetime
import os

import discord
from discord.ext import commands


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
bot = commands.Bot(command_prefix='p!', intents=discord.Intents().all())


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')
    # 2ecc71 Hex code for color embeds


@bot.event
async def on_connect():
    print('Bot connected')


@bot.event
async def on_disconnect():
    print('Bot disconnected')


@bot.event
async def on_ready():
    # Removes 'help' command
    bot.remove_command('help')

    # When bot is ready, send ready message
    await bot.change_presence(activity=discord.Game('Bamboo Simulator'))
    print(f'Logged in as {bot.user.name} ({bot.user.id})\n'
          f'\nLogged in Guilds:')
    for guild in bot.guilds:
        print(f'{guild.name} ({guild.id})')

    # Loads all cogs on startup
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
            print(f'loaded {filename}')

    on_ready_channels = [
        820473911753310208
    ]

    for on_ready_channels in on_ready_channels:
        ch = bot.get_channel(on_ready_channels)
        embed = discord.Embed(title='Bot Connected', color=0x08c744, timestamp=datetime.utcnow())
        signature(embedMessage=embed)
        await ch.send(embed=embed)


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    msg = ctx.message

    if extension.casefold() == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                    print(f'loaded {filename}')
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


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    msg = ctx.message

    if extension.casefold() == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.unload_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                    print(f'unloaded {filename}')
                except:
                    pass
        await ctx.send('Unloaded all extensions')
        await msg.add_reaction('✅')
    else:
        try:
            bot.unload_extension(f'cogs.{extension}')
            await ctx.send(f'Unloaded `{extension}.py`')
            print(f'unloaded {extension}.py')
            await msg.add_reaction('✅')
        except:
            await ctx.send("Extension already unloaded or doesn't exist")
            await msg.add_reaction('❌')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    msg = ctx.message

    if extension.casefold() == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.reload_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                    print(f'reloaded {filename}')
                except:
                    pass
        await ctx.send('Reloaded all extensions')
        await msg.add_reaction('✅')
    else:
        try:
            bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'Reloaded `{extension}.py`')
            print(f'reloaded {extension}.py')
            await msg.add_reaction('✅')
        except:
            await ctx.send("Extension already reloaded or doesn't exist")
            await msg.add_reaction('❌')


@bot.command(name='dev')
@commands.is_owner()
async def dev(ctx, cmd):
    msg = ctx.message

    if cmd == 'unload':
        for filename in os.listdir('./in-dev'):
            if filename.endswith('.py'):
                try:
                    bot.unload_extension(f'in-dev.{filename[:-3]}')
                    print(f'unloaded {filename}')
                except:
                    pass
        await ctx.send('Unloaded all in-development extensions')
        await msg.add_reaction('✅')
    elif cmd == 'load':
        for filename in os.listdir('./in-dev'):
            if filename.endswith('.py'):
                try:
                    bot.load_extension(f'in-dev.{filename[:-3]}')
                    print(f'loaded {filename}')
                except:
                    pass
        await ctx.send('Loaded all in-development extensions')
        await msg.add_reaction('✅')
    elif cmd == 'reload':
        for filename in os.listdir('./in-dev'):
            if filename.endswith('.py'):
                try:
                    bot.reload_extension(f'in-dev.{filename[:-3]}')
                    print(f'reloaded {filename}')
                except:
                    pass
        await ctx.send('Reloaded all in-development extensions')
        await msg.add_reaction('✅')


# Manually updates the seasonal role count
# See cogs/seasonalRole.py
@bot.command(name='updatedisplay', aliases=['ud'])
@commands.is_owner()
async def updateSeasonalRoleDisplay(ctx):
    display_channels = [
        862526927440707614,  # PBT
        863851458583592991,  # BB
    ]

    for channel in display_channels:
        logging_channel = bot.get_channel(863854481773953055)

        try:
            ch = discord.utils.get(ctx.guild.voice_channels, id=channel)
            role = discord.utils.find(lambda r: r.name == 'Sunny 🌞', ctx.guild.roles)

            await ch.edit(name=f'Sunny: {len(role.members)} 🌞')

            embed = discord.Embed(title=f'Display updated manually in guild `{ctx.guild}`', color=0x2ecc71,
                                  description=f'```{ch.name}```', timestamp=datetime.utcnow())
            signature(embed)

            await logging_channel.send(embed=embed)
            print('Display updated manually')
        except AttributeError:
            pass


# run bot
bot.run(token)
