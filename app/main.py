import os
from os.path import join, dirname
from dotenv import load_dotenv

from discord import app_commands
import discord
from dice import roll, DiceBaseException

from server import keep_alive

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

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

keep_alive()

client.run(os.getenv("DISCORD_TOKEN"))
