from __future__ import annotations
import os
import discord

from typing import Optional
from core.embed import Embed
from discord.ext import commands
from logging import getLogger
from settings_file import DISCORD_BOT_STATUS

log = getLogger("Bot")

__all__ = (
    "Bot",
)

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix="-vmp",
            intents=discord.Intents.all(),
            help_command=None,
            activity = discord.Activity(name=DISCORD_BOT_STATUS, type=discord.ActivityType.watching),
            chunk_guild_at_startup=False
        )

    async def setup_hook(self) -> None:
        for file in os.listdir('cogs'):
            if not file.startswith("_") and file.endswith('.py'):
                await self.load_extension(f"cogs.{file[:-3]}")
        
        log.info(f'Logged in as {self.user} (ID: {self.user.id})')

    async def success(
        self, 
        message: str, 
        interaction: discord.Interaction,
        *,
        ephemeral: bool = False,
        embed: Optional[bool] = True
    ) -> Optional[discord.WebhookMessage]: 
        """This function will send a success message."""
        if embed:
            embed_data = Embed(description=message, color=discord.Colour.green())
            embed_data.credits()
            if interaction.response.is_done():  
                return await interaction.followup.send(
                    embed=embed_data,
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed=embed_data,
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    content=f"✅ | {message}",
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                content=f"✅ | {message}",
                ephemeral=ephemeral
            )

    async def error(
        self, 
        message: str, 
        interaction: discord.Interaction,
        *,
        ephemeral: bool = True,
        embed: Optional[bool] = True
    ) -> Optional[discord.WebhookMessage]:  
        """This function will send a success message."""
        if embed:
            embed_data = Embed(description=message, color=discord.Colour.red())
            embed_data.credits()
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed=embed_data,
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed=embed_data,
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    content=f"❌ | {message}",
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                content=f"❌ | {message}",
                ephemeral=ephemeral
            )


