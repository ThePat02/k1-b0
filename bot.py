"""K1-B0 is a discord bot inspired by the character from Danganronpa 3"""

# -----------------------------------------------------------------------------
# Imports

# Import discord library
import discord
from discord.ext import commands

# Import libraries
import requests

# Import cogs
from cogs.greetings import Greetings
from cogs.valorant import Valorant

# Import modules
import utils

# -----------------------------------------------------------------------------
# Constants

COMMAND_PREFIX = "?"
URL = "https://api.henrikdev.xyz/valorant/v1/"
URL_MATCH = "https://api.henrikdev.xyz/valorant/v3/matches/eu/"

COLOR_VALO = 0xFE3939
COLOR_VICTORY = 0x00FF00
COLOR_DEFEAT = 0xFF0000

# -----------------------------------------------------------------------------
# Setup

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    """Runs when the bot is ready"""
    utils.print_line()
    await bot.add_cog(Greetings(bot))
    await bot.add_cog(Valorant(bot))
    wait client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Wingman sleep"))
    print("Beep-bop! K1-B0 is ready to roll!")
    utils.print_line()

# -----------------------------------------------------------------------------
# Run K1-B0
bot.run("MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU")
