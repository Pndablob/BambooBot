import json
from datetime import datetime

import discord
from discord.ext import commands


def load_json(filename):
    with open(filename) as infile:
        return json.load(infile)


class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global blacklisted_words
        blacklisted_words = [
            "fuck", "bitch", "dick", "cock", "pussy", "fag", "slut", "douche", "cunt", "porn", "nigger", "faggot",
            "niggar", "fck", "retarded", "horny", "f​uck", "jizz", "asshole", "cuck", "retard", "dicks", "cocks",
            "vagina", "boob", "pussies", "cunts", "titty", "tittie", "ejaculate", "faggots", "nazi", "nazis", "nigga",
            "niggas", "niggers", "sex", "pedo", "seks", "whore", "anus", "anul", "penis", "hentai", "nude", "cum",
            "rape", "semen"
        ]

    # Filter for blacklisted strings
    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if not isinstance(message.channel,
                          discord.TextChannel) or message.author.id == self.bot.user.id or message.guild.id == 450878205294018560:
            # Only in a text (guild) channel and message was not from bot
            return

        bypass_roles = [
            # PBT
            815952833253605426,  # *
            # TZT
            845340124157181972,  # *
            # BB
            451039471547318272,  # Head Chef
            472842678778724352,  # Intellectual
            723200592742449182,  # pnda
            648234175425675276,  # *
            782437274045382726,  # Pro Bakerator
            673728339076317184,  # Epic Coders
            646106899737083945,  # Hypixel Staffy People
            603719761934942238,  # Creator
        ]

        # Checks if user has a bypass role
        for roles in message.author.roles:
            if roles.id in bypass_roles:
                # Does not blacklist users with bypass roles
                return

        msg = message.content.lower()

        # Checks messages for blacklisted words
        for i in range(len(blacklisted_words)):
            if f' {blacklisted_words[i]} ' in msg or f' {blacklisted_words[i]}' in msg or f'{blacklisted_words[i]} ' in msg or msg.startswith(f'{blacklisted_words[i]}') or msg.endswith(f'{blacklisted_words[i]}'):
                await message.delete()

                embed = discord.Embed(title='Bad Word!', color=0xff0000, timestamp=datetime.utcnow(),
                                      description=f'Your message containing `{blacklisted_words[i]}` was removed')
                await message.author.send(embed=embed)
                print(f'deleting [{blacklisted_words[i]}]')
                break


def setup(bot):
    bot.add_cog(blacklist(bot))
