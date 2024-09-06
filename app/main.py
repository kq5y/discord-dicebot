import os
from os.path import join, dirname
from dotenv import load_dotenv

import discord
from discord import app_commands
from dice import roll, DiceBaseException

from server import keep_alive

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ENABLE_SERVER = os.getenv("ENABLE_SERVER")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set")

if not ENABLE_SERVER:
    ENABLE_SERVER_BOOL = False
else:
    ENABLE_SERVER_BOOL = ENABLE_SERVER.lower() == "true"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/roll"))
    await tree.sync()
    print(f"Bot is ready as {client.user.name}")

@tree.command(name="roll", description="Rolls a dice")
@app_commands.describe(string="The dice to roll", private="Whether the result should be private")
async def dice(interaction: discord.Interaction, string: str, private: bool = False):
    try:
        result = roll(string)
        await interaction.response.send_message(f"Result: {result}", ephemeral=private)
    except DiceBaseException as e:
        await interaction.response.send_message(str(e), ephemeral=private)

if ENABLE_SERVER_BOOL:
    keep_alive()

client.run(DISCORD_TOKEN)
