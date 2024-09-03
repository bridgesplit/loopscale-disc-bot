from __future__ import annotations

import discord
from discord import app_commands
from core import Bot, Embed
from core.util import get_user_name
from . import Plugin
from typing import Literal
from core.api import _get_user_points, _get_user_waitlist_position, _top_10_leaderboard
from settings_file import POINTS_THRESHOLD, CLAIM_ROLE_ID

class Commands(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command(name="points", description="View your points.")
    async def points_command(self, interaction: discord.Interaction,
        user: discord.User | None
    ):  
        
        # Check if the user parameter is provided and if the user has 'Manage Server' permission
        if user and not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                f"You don't have permission to view another user's points. Use the `/{interaction.command.name}` command without the user parameter to view your points.", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer(thinking=True, ephemeral=False)
        target = user or interaction.user

        user_points = await _get_user_points(target.id, target.name)
        if not user_points:
            await self.bot.error(
                f"Unable to fetch your points. Please connect your discord to the platform first.", 
                interaction
            )
            return
        
        try:
            # check if points greater than the points_threshold
            if user_points > POINTS_THRESHOLD:
                # give user role
                role_to_give = interaction.guild.get_role(CLAIM_ROLE_ID)
                await target.add_roles(role_to_give)
        except:
            # this should only happen:
            # - if the user already has the role, 
            # - or the bot role is below the role to give in the discord server's role heirarchy, 
            # - or if the bot doesn't have the permission to give the role.
            # So, if the user doesn't get the role please check the role heirarchy and bot permissions
            # if you notify the user if the role add fail here, if you want.
            pass
            
        prefix = "Your" if not user else f"{user}'s"
        await self.bot.success(
            f"{prefix} total points are `{user_points}`",
            interaction
        )

    @app_commands.guild_only()
    @app_commands.command(name="waitlist-rank", description="View your current waitlist rank.")
    async def waitlist_rank_command(self, interaction: discord.Interaction,
        user: discord.User | None
    ):  
        
        # Check if the user parameter is provided and if the user has 'Manage Server' permission
        if user and not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                f"You don't have permission to view another user's waitlist rank. Use the `/{interaction.command.name}` command without the user parameter to view your waitlist rank.", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer(thinking=True, ephemeral=False)
        target = user or interaction.user

        user_rank= await _get_user_waitlist_position(target.id, target.name)

        if not user_rank:
            await self.bot.error(
                f"Unable to fetch your waitlist rank. Please connect your discord to the platform first.", 
                interaction
            )
            return
        
        if user_rank.get('userRank') == 0:
            message = "🥳 ➰  User is already off the waitlist! "
        else:
            message = f"User's waitlist rank is `{user_rank}`"

        await self.bot.success(
            message,
            interaction
        )

    @app_commands.guild_only()
    @app_commands.command(name="leaderboard", description="Top 10 users based on points or waitlist rank.")
    async def leaderboard_command(self, interaction: discord.Interaction,
        type: Literal["points", "waitlist"]
    ):         
        await interaction.response.defer(thinking=True, ephemeral=False)
        
        leaderboard_raw_data = await _top_10_leaderboard(type)
        if not leaderboard_raw_data:
            await self.bot.error(
                f"Unable to fetch top 10 leaderboard.", 
                interaction
            )
            return
    
        user_list = []
        for index, user in enumerate(leaderboard_raw_data, start=1):
            if type == "points":
                user_info_to_display = f"`{user.get('totalPoints')}`"
            else:
                user_info_to_display = f"`Rank-{user.get('waitlistRank')}`"
            
            symbol, user_name = get_user_name(user)
                
            if index == 1:
                user_list.append(f"> 🥇 - {symbol} - **{user_name}**: {user_info_to_display}")
            elif index == 2:
                user_list.append(f"> 🥈 - {symbol} - **{user_name}**: {user_info_to_display}")
            elif index == 3:
                user_list.append(f"> 🥉 - {symbol} - **{user_name}**: {user_info_to_display}\n")
            else:
                user_list.append(f"`{index}` - {symbol} - **{user_name}**: {user_info_to_display}")

        embed_user_list = '\n'.join(user_list)
        
        embed = Embed(title=f"🏆 Server Leaderboard - {type}", description=f"This leaderboard displays the Top 10 members by {type}.\n\n{embed_user_list}")
        embed.credits()

        await interaction.followup.send(embed=embed)
        
async def setup(bot: Bot):
    await bot.add_cog(Commands(bot))