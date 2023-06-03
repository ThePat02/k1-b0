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


class ValorantUser:
    """A valornt user object that contains the user's information"""

    def __init__(self, name, tag, card, level):
        self.name = name
        self.tag = tag
        self.card = card
        self.level = level


class ValorantMatch:
    """A valorant match object that contains the match's information"""

    def __init__(self, location, mode, team, result):
        self.location = location
        self.mode = mode
        self.team = team
        self.result = result


bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    """Runs when the bot is ready"""
    utils.print_line()
    await bot.add_cog(Greetings(bot))
    await bot.add_cog(Valorant(bot))
    print("Beep-bop! K1-B0 is ready to roll!")
    utils.print_line()

# -----------------------------------------------------------------------------
# Run K1-B0
bot.run("MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU")
