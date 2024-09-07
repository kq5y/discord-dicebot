import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv

import discord
import requests
from discord import app_commands

from server import keep_alive

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

logger = logging.getLogger("discord")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ENABLE_SERVER = os.getenv("ENABLE_SERVER")
BCDICE_URL = os.getenv("BCDICE_URL")
BCDICE_SYSTEM = os.getenv("BCDICE_SYSTEM")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set")

if not ENABLE_SERVER:
    ENABLE_SERVER_BOOL = False
else:
    ENABLE_SERVER_BOOL = ENABLE_SERVER.lower() == "true"

if not BCDICE_URL:
    BCDICE_URL = "https://bcdice.kazagakure.net"

if not BCDICE_SYSTEM:
    BCDICE_SYSTEM = "DiceBot"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/roll"))
    await tree.sync()
    logger.info("Bot is ready as %s", client.user.name)

@tree.command(name="roll", description="Rolls a dice")
@app_commands.describe(command="The dice to roll", private="Whether the result should be private")
async def dice(interaction: discord.Interaction, command: str, private: bool = False):
    try:
        result = requests.get(f"{BCDICE_URL}/v2/game_system/{BCDICE_SYSTEM}/roll", params={"command": command})
        result_json = result.json()
        if result.status_code != 200 or (not result_json["ok"]):
            raise Exception(result_json["reason"])
        await interaction.response.send_message(result_json["text"], ephemeral=private)
    except Exception as e:
        await interaction.response.send_message(str(e), ephemeral=private)
        logger.error("Error rolling dice", exc_info=e)

@tree.command(name="bchelp", description="Shows bcdice help")
async def bchelp(interaction: discord.Interaction):
    try:
        result = requests.get(f"{BCDICE_URL}/v2/game_system/{BCDICE_SYSTEM}")
        result_json = result.json()
        if result.status_code != 200 or (not result_json["ok"]):
            raise Exception(result_json["reason"])
        help_message = result_json["help_message"]
        help_message = help_message.replace("*", "\\*").replace("_", "\\_").replace("~", "\\~")
        await interaction.response.send_message(help_message, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(str(e), ephemeral=True)
        logger.error("Error getting help", exc_info=e)

if ENABLE_SERVER_BOOL:
    keep_alive()

client.run(DISCORD_TOKEN)
