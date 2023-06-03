"""K1-B0 is a discord bot inspired by the character from Danganronpa 3"""

# -----------------------------------------------------------------------------
# Imports

# Import discord library
import discord
from discord.ext import commands, tasks

# Import libraries
import datetime

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
    print("Beep-bop! K1-B0 is ready to roll!")
    utils.print_line()

    change_status.start()

@tasks.loop(minutes=30)
async def change_status():
    """Changes the bot's status"""
    # Get time
    now = datetime.datetime.now() 
    status = "Wingman do stuff"

    hour = now.hour + 2
    if hour >= 24: hour -= 24

    if hour >= 6 and hour < 9:
        status = "Wingman wake up"
    elif hour >= 9 and hour < 12:
        status = "Wingman plant the spike"
    elif hour >= 12 and hour < 15:
        status = "Wingman eat a snack"
    elif hour >= 15 and hour < 18:
        status = "Wingman play with Dizzy"
    elif hour >= 18 and hour < 20:
        status = "Wingman eat dinner"
    elif hour >= 20 and hour < 22:
        status = "Wingman working out"
    elif hour >= 22 and hour < 24:
        status = "Wingman sleep"
    elif hour >= 0 and hour < 6:
        status = "Wingman sleeping deeply"

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))


# -----------------------------------------------------------------------------
# Run K1-B0
bot.run("MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU")
