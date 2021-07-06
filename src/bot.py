import datetime

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


# Send bot latency
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


# Echos a message
@bot.command(aliases=['say'])
async def echo(ctx, *, msg):
    await ctx.message.delete()

    ch = bot.get_channel(850159250629722123)
    embed = discord.Embed(title='Echo 📣', description=f'Echoed message by {ctx.message.author.mention}\n',
                          color=0x2ecc71, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='Message:', value=f'```{msg}```', inline=False)
    embed.add_field(name='Guild:', value=f'```{ctx.message.guild}```', inline=False)

    await ch.send(embed=embed)


# DM's a user a message
@bot.command(name='message', aliases=['dm', 'poke'])
async def _message(ctx, user: discord.Member, *, msg):
    await ctx.message.delete()
    await user.send(msg)

    ch = bot.get_channel(850159250629722123)
    embed = discord.Embed(title='Boop! ❗', description=f'{user.mention} was poked', color=0x2ecc71,
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name='Message:', value=f'```{msg}```', inline=False)
    embed.add_field(name='Guild:', value=f'```{ctx.message.guild}```', inline=False)
    await ch.send(embed=embed)


# Sends info about a user
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.message.author

    fields = [
        ('Username', user.mention, False),
        ('User ID', user.id, False),
        ('Highest Role', user.top_role, False),
        ('Create Date', user.created_at, False),
        ('Join Date', user.joined_at, False)
    ]
    embed = discord.Embed(title='User Info:', color=0x0565ff, timestamp=datetime.datetime.utcnow())
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


# Sky.shiiyu.moe command
@bot.command(aliases=['sc', 'scs'])
async def skycrypt(ctx, ign, profile):
    await ctx.send(f'https://sky.shiiyu.moe/stats/{ign}/{profile}')


# Purges a given number of messages
@bot.command(aliases=['purge'])
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount):
    await ctx.channel.purge(limit=int(amount) + 1)
    await ctx.send(f'Purged **{amount}** messages in {ctx.channel.mention}')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention}, You do not have permission to use this command')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.message.author.mention}, Please enter all required arguments')
    else:
        raise error


# Sets the slowmode of a channel
@bot.command(aliases=['sm'])
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, delay: int):
    await ctx.channel.edit(slowmode_delay=delay)
    await ctx.send(f'Set the slowmode delay in {ctx.channel.mention} to {delay} seconds')


# Suggestion command
@bot.command()
@commands.cooldown(1, 7200)
async def suggest(ctx, sugtype=None, *, suggestion=None):
    global sbaSuggestionEmbed
    global discordSuggestionEmbed

    # Gets channels for waitlist, logging, and approved suggestions
    suggestionLogsChannel = bot.get_channel(851221149378805802)
    suggestionWaitlistChannel = bot.get_channel(844926347599151154)
    suggestionApproveChannel = bot.get_channel(851204911533785088)

    def check(reaction, user):
        return user == ctx.message.author

    if suggestion is None:
        suggestion = 'Empty Suggestion'

    # Suggestion for SBA
    if sugtype == 'sba':
        await ctx.message.add_reaction('✅')

        # Creates embedded message for a suggestion
        sbaSuggestionEmbed = discord.Embed(title=f'New SBA Suggestion by {ctx.message.author}',
                                           description=f'```{suggestion}```', color=0xF5A623,
                                           timestamp=datetime.datetime.utcnow())
        signature(embedMessage=sbaSuggestionEmbed)
        sbaSuggestionEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

        # Sends embed in the waitlist channel for a moderator to approve
        msg = await suggestionWaitlistChannel.send(embed=sbaSuggestionEmbed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        try:
            # Waiting for a reaction response
            reaction, user = await bot.wait_for('reaction_add', check=check)
            if str(reaction) == '✅':
                # If approved, send to the approved suggestions channel
                await suggestionApproveChannel.send(embed=sbaSuggestionEmbed)
                lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)
                await lastMessage.add_reaction('✅')
                await lastMessage.add_reaction('❌')

                # Log approval
                logEmbed = discord.Embed(title=f'SBA Suggestion was `Approved`', description=f'```{suggestion}```',
                                         color=0x00ff00, timestamp=datetime.datetime.utcnow())
                logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                signature(embedMessage=logEmbed)
                await suggestionLogsChannel.send(embed=logEmbed)

                # Delete suggestion from waitlist
                await lastMessage.delete()
            elif str(reaction) == '❌':
                # If rejected, delete message
                lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)

                # Log deletion
                logEmbed = discord.Embed(title=f'SBA Suggestion was `Rejected`', description=f'```{suggestion}```',
                                         color=0xff0000, timestamp=datetime.datetime.utcnow())
                logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                signature(embedMessage=logEmbed)
                await suggestionLogsChannel.send(embed=logEmbed)

                # Delete suggestion from waitlist
                await lastMessage.delete()
            else:
                suggestionLogsChannel.send('Invalid Emoji')
        finally:
            pass
    # Suggestions for Discord
    elif sugtype == 'discord' or 'disc' or 'd':
        await ctx.message.add_reaction('✅')

        # Creates embedded message for suggestion
        discordSuggestionEmbed = discord.Embed(title=f'New Discord Suggestion by {ctx.message.author}',
                                               description=f'```{suggestion}```', color=0x5865F2,
                                               timestamp=datetime.datetime.utcnow())
        signature(embedMessage=discordSuggestionEmbed)
        discordSuggestionEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

        # Sends embed in the waitlist channel for a moderator to approve
        msg = await suggestionWaitlistChannel.send(embed=discordSuggestionEmbed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        try:
            # Waiting for a reaction response
            reaction, user = await bot.wait_for('reaction_add', check=check)
            if str(reaction) == '✅':
                # If approved, send to the approved suggestions channel
                await suggestionApproveChannel.send(embed=discordSuggestionEmbed)
                lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)
                await lastMessage.add_reaction('✅')
                await lastMessage.add_reaction('❌')

                # Log approval
                logEmbed = discord.Embed(title=f'Discord Suggestion was `Approved`', description=f'```{suggestion}```',
                                         color=0x00ff00, timestamp=datetime.datetime.utcnow())
                logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                signature(embedMessage=logEmbed)
                await suggestionLogsChannel.send(embed=logEmbed)

                # Delete suggestion from waitlist
                await lastMessage.delete()
            elif str(reaction) == '❌':
                lastMessage = await suggestionWaitlistChannel.fetch_message(reaction.message.id)

                # Log deletion
                logEmbed = discord.Embed(title=f'Discord Suggestion was `Rejected`', description=f'```{suggestion}```',
                                         color=0xff0000, timestamp=datetime.datetime.utcnow())
                logEmbed.add_field(name='User ID:', value=ctx.message.author.id, inline=False)
                logEmbed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                signature(embedMessage=logEmbed)
                await suggestionLogsChannel.send(embed=logEmbed)

                # Delete suggestion from waitlist
                await lastMessage.delete()
            else:
                suggestionLogsChannel.send('Invalid emoji')
        finally:
            pass
    elif sugtype is None:
        await ctx.message.add_reaction('❌')
        embed = discord.Embed(title='Error', description='Please enter `sba` or `discord` for your suggestion type',
                              color=0xff0000, timestamp=datetime.datetime.utcnow())
        signature(embedMessage=embed)
        await ctx.send(embed=embed)


@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'{ctx.message.author.mention}\n{error}')


# @bot.command(name='manualsuggest', alliases=['approve', 'ms'])
# @commands.has_any_role()
# async def approveSuggestion():


# Color role command
@bot.command(name='color')
@commands.has_any_role(
    815952833253605426,  # * PBT
    845089203788578857,  # nerd TZT
    723200592742449182,  # Pnda Role BB
    653624748311576632,  # Staff BB
    578281324914278410,  # Collaborator BB
    617803927240310823,  # Ebic Translator BB
    733448745517187134,  # Patron BB
    614357920351649805,  # Nitro Booster BB
    673728339076317184,  # Epic Coders BB
    623288545439645706,  # Partner BB
    646106899737083945,  # Hypixel Staffy People BB
    603719761934942238,  # Creator BB
    825256068607115275,  # 1b Giveaway Donator BB
    792168173448986624,  # 500m Giveaway Donator
    798764352823623720  # Super Baker (50) BB
)
@commands.bot_has_permissions(manage_roles=True)
async def _color(ctx, *, color=None):
    global color_guild
    color_guild = []
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
    colors_203 = [
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
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                if role in user.roles:
                    await user.remove_roles(role)
        elif guild == 756305026627928175:  # TZT
            for role_id in colors_203:
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                if role in user.roles:
                    await user.remove_roles(role)
        elif guild == 450878205294018560:  # BB
            for role_id in colors_BB:
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                if role in user.roles:
                    await user.remove_roles(role)

    if color.title() == 'Clear':
        await clear_color_roles()

        embed = discord.Embed(title='Color Roles Cleared', description=f'Your color roles have been removed',
                              color=0xffffff, timestamp=datetime.datetime.utcnow())
        signature(embedMessage=embed)
        await ctx.send(embed=embed)
    else:
        await clear_color_roles()

        role = discord.utils.find(lambda r: r.name == f'Color - {color.title()}', ctx.guild.roles)
        await user.add_roles(role)
        embed = discord.Embed(title='Color Role Given', description=f'Your color is now: `{color.title()}`',
                              color=role.color, timestamp=datetime.datetime.utcnow())
        signature(embedMessage=embed)
        await ctx.send(embed=embed)


@_color.error
async def _color_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed = discord.Embed(title='Insignificant Permission', color=0xff0000, timestamp=datetime.datetime.utcnow(),
                              description='You lack a required role to use this command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.message.author.mention}, Please enter the required arguments')
    else:
        raise error

# run bot
bot.run(token)
