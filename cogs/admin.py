import io
import logging
import textwrap
import traceback
from contextlib import redirect_stdout
from bot import initial_extensions
from cogs.utils.constants import BOT_COLOR

from discord.ext import commands
import discord

log = logging.getLogger('discord')


class Admin(commands.Cog):
    """Admin-only commands"""

    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content: str) -> str:
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(name='sync')
    @commands.is_owner()
    @commands.guild_only()
    async def sync_commands(self, ctx, glo=False):
        if glo:
            await self.bot.tree.sync()
            await ctx.send(f"Synced application commands globally")
        else:
            await self.bot.tree.copy_global_to(guild=ctx.guild)
            await ctx.send(f"Synced application commands to `{ctx.guild.name}`")

    def get_syntax_error(self, e: SyntaxError) -> str:
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True, aliases=['l'])
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        msg = ctx.message

        if module == "all":
            try:
                for module in initial_extensions:
                    await self.bot.load_extension(module)
                    log.info(f"Loaded extension: {module}")
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            await msg.add_reaction('✅')
        else:
            try:
                await self.bot.load_extension(f"cogs.{module}")
                log.info(f"Loaded extension: cogs.{module}")
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            else:
                await msg.add_reaction('✅')

    @commands.command(hidden=True, aliases=['ul'])
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        msg = ctx.message

        if module == "all":
            try:
                for module in initial_extensions:
                    await self.bot.unload_extension(module)
                    log.info(f"Unloaded extension: {module}")
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            await msg.add_reaction('✅')
        else:
            try:
                await self.bot.unload_extension(f"cogs.{module}")
                log.info(f"Unloaded extension: cogs.{module}")
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            else:
                await msg.add_reaction('✅')

    @commands.group(name='reload', aliases=['rl'], hidden=True, invoke_without_command=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        msg = ctx.message

        if module == "all":
            try:
                for module in initial_extensions:
                    await self.bot.reload_extension(module)
                    log.info(f"Reloaded extension: {module}")
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            await msg.add_reaction('✅')
        else:
            try:
                await self.bot.reload_extension(f"cogs.{module}")
                log.info(f"Reloaded extension: cogs.{module}")
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            else:
                await msg.add_reaction('✅')

    @commands.command(hidden=True, name='eval', aliases=['ev'])
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        no_evals = ['token', 'delete', 'exit']
        if any(w in body for w in no_evals):
            await ctx.send(f"Found prohibited string(s) ... terminating eval")
            return

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


async def setup(bot):
    await bot.add_cog(Admin(bot))
