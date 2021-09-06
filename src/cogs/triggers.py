from datetime import datetime
import random

import discord
from discord.ext import commands


def add_author(embedMessage, author):
    # Signs embedded messages with a signature.
    embedMessage.set_footer(text=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)


class pingfaq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    @commands.is_owner()
    async def on_message(self, message):
        # Pass context
        ctx = await self.bot.get_context(message)

        if not isinstance(message.channel, discord.TextChannel) or message.author == self.bot.user.id:
            # Only in a text channel and message was not from bot
            return
        if not message.author.id == 317751950441447435:
            # Only for bot owner
            return

        replies = [
            "Pong!",
            "Hey cut it out!",
            "I don't like being pinged either <a:rageblob:810669822060134440>",
            "Hello!",
            "Growing bamboo by the mile!",
            "Hiii 👋",
            "Pnda is pretty cool",
            "Did you know certain species of bamboo can grow up to 36 inches per day?",
            "Sorry, wrong member",
            f"||<@317751950441447435>|| blame {message.author.mention} 😏",
            f"Have a ping in return {message.author.mention}",
            "e",
            f"Hey {message.author.mention}, How Play Game?",
            f"Sometimes I try to ping bots and this happens 😦",
        ]

        # Replies a cool message if pinged
        if self.bot.user.mentioned_in(message):
            rand_index = random.randint(0, len(replies))
            print(rand_index)

            if rand_index == (len(replies)):
                embed = discord.Embed(title=f'Problem?', color=0x2ECC71, timestamp=datetime.utcnow(),
                                      description=f'Click [here](https://www.youtube.com/watch?v=2ocykBzWDiM) 🙂')
                embed.set_footer(text=f'Triggered by {message.author}',
                                 icon_url=message.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send(replies[rand_index])

        # Dead chat
        elif "dead chat" in message.content.lower():
            if "chat killer" in str(message.author.nick).lower():
                await ctx.send(f"Hey don't look at me; blame yourself! <a:trolling:878127387336933376>")
            elif await self.bot.is_owner(message.author):
                await ctx.send(f"What are you going to do about it? Ping everyone? 🙄")
            else:
                await ctx.send(f"Complaining won't do anything about it <a:rageblob:810669822060134440>")


def setup(bot):
    bot.add_cog(pingfaq(bot))
