# TODO:
#  music cog
#  global command error handling
#  pagination (discord.ext.menus)?
#  custom help commands
#  organize commands into main and sub commands
#  git push pull using commands
#  vps hosting


import logging
from datetime import datetime
from cogs.utils.constants import *

from discord.ext import commands
import discord

log = logging.getLogger('discord')

initial_extensions = (
    'cogs.admin',
    'cogs.stats',
    'cogs.rng',
    'cogs.moderation',
    'cogs.info',
    'cogs.chat',
    'cogs.music',
)


class BambooBot(commands.Bot):
    def __init__(self):
        self.start_time = None
        super().__init__(
            command_prefix=['p!', 'P!'],
            description="I'm a multipurpose Discord bot with some neat utilities",
            allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True),
            intents=discord.Intents.all(),
            pm_help=None,
            help_command=None,
            chunk_guilds_at_startup=False,
            enable_debug_events=True,
        )

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(PBT_ID))

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                log.info(f"Loaded extension: {extension}")
            except Exception as e:
                log.exception(f"Failed to load extension {extension}")

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.start_time = datetime.utcnow()

        log.info(f"Bot ready: {self.user} (ID: {self.user.id})")
        log.info(f"Bot started in {datetime.utcnow().timestamp() - run_time} seconds")


if __name__ == '__main__':
    run_time = datetime.utcnow().timestamp()

    token = open("token.txt").readline().rstrip()

    bot = BambooBot()

    # logging
    file_handler = logging.FileHandler(filename='bamboo_bot.log', encoding='utf-8', mode='w')
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
    file_handler.setFormatter(fmt)
    discord.utils.setup_logging()

    bot.run(token=token, reconnect=True, log_handler=file_handler, log_formatter=fmt, log_level=logging.INFO)
