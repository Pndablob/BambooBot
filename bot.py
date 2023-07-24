import logging
from datetime import datetime
from cogs.utils.constants import PBT

from discord.ext import commands
import discord

log = logging.getLogger('discord')

initial_extensions = (
    'cogs.admin',
    'cogs.stats',
    'cogs.rng',
    'cogs.mod',
    'cogs.info',
    'cogs.chat',
    'cogs.music',
)


# TODO slash commands
# TODO music cog
# TODO command error handling
# TODO pagination (discord.ext.menus)?
# TODO custom help commands
# TODO organize commands into main and sub commands
# TODO git push pull using commands
# TODO vps hosting


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
        await self.tree.sync(guild=discord.Object(PBT.id))

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
    discord.utils.setup_logging(handler=file_handler, formatter=fmt, level=logging.DEBUG)

    bot.run(token=token, reconnect=True)
