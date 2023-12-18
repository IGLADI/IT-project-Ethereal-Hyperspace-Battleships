from discord import app_commands
import discord
from discord.ext import commands

import data
from player import Player
from utils import check_player_exists
from ui.simple_banner import ErrorBanner, NormalBanner, SuccessBanner


class GeneralCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Provides a list of bot commands")
    async def help(self, interaction: discord.Interaction):
        # Welcome message and tutorial
        help_message = "Welcome to Ethereal Hyperspace Battleships!\n"
        help_message += "To start out, please type /register followed by /tutorial.\n"
        # Command list
        help_message += "Here is a list of commands:\n"
        help_message += "/help - Get help\n"
        help_message += "/guild - Get guild info\n"
        help_message += "/resources - Get info on resources and mining\n"
        help_message += "/balance - Check your money\n"
        help_message += "/pay - Give money to a player\n"
        banner = NormalBanner(text=help_message, user=interaction.user)
        await interaction.response.send_message(embed=banner.embed, ephemeral=True)

    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        if await check_player_exists(interaction) is False:
            return

        player = data.players[interaction.user]
        balance = player.money
        balance_banner = NormalBanner(user=interaction.user, text=f"Your current balance is ${balance}.")
        await interaction.response.send_message(embed=balance_banner.embed, ephemeral=True)

    # TODO maybe add displayname
    # ! (still keep id and add a check so that only one user can create an account with a name)
    @app_commands.command(name="register", description="Register as a player")
    async def register(self, interaction: discord.Interaction):
        if interaction.user not in data.players:
            player = Player(interaction.user)
            data.players[interaction.user] = player
            banner = SuccessBanner(text="Welcome to Ethereal Hyperspace Battleships!", user=interaction.user)
            await interaction.response.send_message(embed=banner.embed, ephemeral=True)
        else:
            banner = ErrorBanner(text="You are already registered as a player.", user=interaction.user)
            await interaction.response.send_message(embed=banner.embed, ephemeral=True)

    @app_commands.command(name="where_am_i", description="Get your location info")
    async def where_am_i(self, interaction: discord.Interaction):
        """Returns the location of the player"""
        if await check_player_exists(interaction) is False:
            return

        player = data.players[interaction.user]
        player_location = player.ship.location
        location_name = player_location.is_planet()
        banner = NormalBanner(
            text=f"You are currently at {player_location}, also known as {location_name}.", user=interaction.user
        )
        await interaction.response.send_message(embed=banner.embed, ephemeral=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(GeneralCommands(client))
