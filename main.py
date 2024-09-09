from __future__ import annotations

import os
from core import Bot
import discord
import typing
from discord.ext import commands
from asyncio import run
from discord import utils
from dotenv import load_dotenv
from enum import Enum

# Load the .env file
load_dotenv()

class Env(Enum):
    STAGING = 'staging'
    PROD = 'prod'

# Change this to switch environments
# Use Loopscale (blue icon) for prod, and Loopscale Bot Tester (PicoSol photo) for testing
CURRENT_ENV = Env.PROD

# Access the variable, replace with 'BOT_STAGING_TOKEN' if want to do staging bot.
BOT_TOKEN = os.getenv('LOOPSCALE_BOT_MAIN_TOKEN')
bot = Bot()

# !sync id_1 id_2 -> syncs guilds with id 1 and 2
@bot.command()
@commands.is_owner()
async def sync(
    ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None
    ) -> None:
        if not guilds:
            # sync current guild
            if spec == "~":
                synced_commands = await ctx.bot.tree.sync(guild=ctx.guild)

            # copies all global app commands to current guild and syncs
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced_commands = await ctx.bot.tree.sync(guild=ctx.guild)

            # clears all commands from the current guild target and syncs (removes guild commands)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced_commands = []
            
            # global sync
            else:
                synced_commands = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced_commands)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

#load cogs
@bot.command()
@commands.is_owner()
async def load(ctx: commands.Context, extension):
    try:
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'`cogs.{extension} loaded`')
    except Exception as error:
        await ctx.send(f"FAILED TO LOAD COG - {error}")

#unload cogs
@bot.command()
@commands.is_owner()
async def unload(ctx: commands.Context, extension):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'`cogs.{extension} unloaded`')
    except Exception as error:
        await ctx.send(f"FAILED TO UNLOAD COG - {error}")

#reload cogs
@bot.command()
@commands.is_owner()
async def reload(ctx: commands.Context, extension):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'`cogs.{extension} reloaded`')
    except Exception as error:
        await ctx.send(f"FAILED TO RELOAD COG - {error}")

async def main():
    utils.setup_logging()
    async with bot:
        await bot.start(BOT_TOKEN, reconnect=True)

if __name__ == '__main__':
    run(main())