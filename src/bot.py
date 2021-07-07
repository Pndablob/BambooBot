import datetime
import os
import discord
from discord.ext import commands


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
bot = commands.Bot(command_prefix='p!')


def signature(embedMessage):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'Bamboo Bot by Pnda#9999',
                            icon_url='https://cdn.discordapp.com/emojis/851191181315538965.png?v=1')


@bot.command()
async def load(ctx, extension):
    msg = ctx.message

    if extension.casefold() == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                except:
                    pass
        await ctx.send('Loaded all extensions')
        await msg.add_reaction('✅')
    else:
        try:
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension} extension')
            await msg.add_reaction('✅')
        except:
            await ctx.send("Extension already loaded or doesn't exist")
            await msg.add_reaction('❌')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    msg = ctx.message

    if extension.casefold() == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.reload_extension(f'cogs.{filename[:-3]}')  # Cut last 3 char (.py)
                except:
                    pass
        await ctx.send('Reloaded all extensions')
        await msg.add_reaction('✅')
    else:
        try:
            bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'Reloaded {extension} extension')
            await msg.add_reaction('✅')
        except:
            await ctx.send("Extension already reloaded or doesn't exist")
            await msg.add_reaction('❌')


@bot.event
async def on_connect():
    print('Bot connected')


@bot.event
async def on_disconnect():
    print('Bot disconnected')


@bot.event
async def on_ready():
    # When bot is ready, send ready message
    await bot.change_presence(activity=discord.Game('Bamboo Simulator'))
    print(f'Logged in as {bot.user.name} ({bot.user.id})\n'
          f'\nLogged in Guilds:')
    for guild in bot.guilds:
        print(f'{guild} ({guild.id})')

    on_ready_channels = [
        820473911753310208
    ]

    for on_ready_channels in on_ready_channels:
        ch = bot.get_channel(on_ready_channels)
        embed = discord.Embed(title='Bot Connected', color=0x08c744, timestamp=datetime.datetime.utcnow())
        signature(embedMessage=embed)
        await ch.send(embed=embed)

# run bot
bot.run(token)
