from __future__ import annotations

import discord
from discord import app_commands
from core import Bot, Embed
from core.util import get_user_name
from . import Plugin
from typing import Literal
from core.api import _get_user_points, _get_user_waitlist_position, _top_10_leaderboard, _mutate_user_points
from settings_file import POINTS_THRESHOLD_WAITLIST, CLAIM_ROLE_WAITLIST, POINTS_THRESHOLD_SUPER_LOOPER, CLAIM_ROLE_SUPER_LOOPER, CLAIM_ROLE_BETA_LOOPER

class Commands(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    ###############################
    ####### POINTS COMMAND ########
    ###############################
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="points", description="View your points.")
    async def points_command(self, interaction: discord.Interaction,
        user: discord.User | None
    ):  
        
        # Check if the user parameter is provided and if the user has 'Manage Messages' permission
        if user and not interaction.user.guild_permissions.manage_messages:
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
            await assign_roles_based_on_points(interaction, target, user_points)
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

    @points_command.error
    async def points_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            seconds = error.retry_after
            await interaction.response.send_message(f"Command on cooldown!. You can use the command again after {int(seconds)} seconds.", ephemeral=True)

    ###############################
    ## POINTS AWARD RANK COMMAND ##
    ###############################
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="award", description="Award points.")
    async def award_points_command(self, interaction: discord.Interaction, user: discord.User, points: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                f"You don't have permission to use this`/{interaction.command.name}` command.", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer(thinking=True, ephemeral=False)
        target = user

        if points > 500 and not interaction.user.guild_permissions.manage_guild:
            await self.bot.error(
                f"You are unable to assign more than 500 points at a time.",
                interaction
            )
            return
        
        if points < 1:
            await self.bot.error(
                f"You are unable to assign negative points. 🤡",
                interaction
            )
            return

        user_mutate_result = await _mutate_user_points(target.id, points)
        if not user_mutate_result:
            await self.bot.error(
                f"<@{target.id}> a team member just tried to award you points, but you haven't connected your Discord to the app yet.", 
                interaction
            )
            return
        
        await self.bot.success(
            f"🎉🎉 <@{target.id}> has been awarded {points} points 🎉🎉",
            interaction
        )
        return

    @award_points_command.error
    async def award_points_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            seconds = error.retry_after
            await interaction.response.send_message(f"Command on cooldown!. You can use the command again after {int(seconds)} seconds.", ephemeral=True)

    ###############################
    #### WAITLIST RANK COMMAND ####
    ###############################
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="waitlist-rank", description="View your current waitlist rank.")
    async def waitlist_rank_command(self, interaction: discord.Interaction,
        user: discord.User | None
    ):  
        
        # Check if the user parameter is provided and if the user has 'Manage Server' permission
        if user and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                f"You don't have permission to view another user's waitlist rank. Use the `/{interaction.command.name}` command without the user parameter to view your waitlist rank.", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer(thinking=True, ephemeral=False)
        target = user or interaction.user

        user_rank = await _get_user_waitlist_position(target.id, target.name)

        if not user_rank:
            await self.bot.error(
                f"Unable to fetch your waitlist rank. Please connect your discord to the platform first.", 
                interaction
            )
            return
        
        if user_rank.get('userRank') == None:
            message = "🥳 ➰  User is already off the waitlist!"
            await assign_role(interaction, target, CLAIM_ROLE_BETA_LOOPER)
        else:
            message = f"User's waitlist rank is `{user_rank.get('userRank')}`"

        await self.bot.success(
            message,
            interaction
        )

    @waitlist_rank_command.error
    async def waitlist_rank_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            seconds = error.retry_after
            await interaction.response.send_message(f"Command on cooldown!. You can use the command again after {int(seconds)} seconds.", ephemeral=True)

    ###############################
    ##### LEADERBOARD COMMAND #####
    ###############################
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
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

    @leaderboard_command.error
    async def leaderboard_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            seconds = error.retry_after
            await interaction.response.send_message(f"Command on cooldown!. You can use the command again after {int(seconds)} seconds.", ephemeral=True)

async def setup(bot: Bot):
    await bot.add_cog(Commands(bot))
      
async def setup(bot: Bot):
    await bot.add_cog(Commands(bot))

async def assign_role(interaction, target, role_id: int):
    try:
        role = interaction.guild.get_role(role_id)
        if role is not None:
            await target.add_roles(role)
    except Exception:
        # Role assignment failed, but we're not logging or notifying
        pass

async def assign_roles_based_on_points(interaction, target, user_points: int):
    role_thresholds = [
        (POINTS_THRESHOLD_WAITLIST, CLAIM_ROLE_WAITLIST),
        (POINTS_THRESHOLD_SUPER_LOOPER, CLAIM_ROLE_SUPER_LOOPER)
    ]

    for threshold, role_id in role_thresholds:
        if user_points > threshold:
            await assign_role(interaction, target, role_id)