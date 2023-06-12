"""K1-B0 is a discord bot inspired by the character from Danganronpa 3"""

# -----------------------------------------------------------------------------
# Imports

# Import libraries
import datetime

# Import discord library
import discord
from discord.ext import commands, tasks

# Import cogs
from cogs.essentials import Essentials
from cogs.valorant import Valorant

# Import modules
import utils

# -----------------------------------------------------------------------------
# Constants

COMMAND_PREFIX = "?"

# -----------------------------------------------------------------------------
# Setup

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is ready"""
    utils.print_line()

    await bot.add_cog(Essentials(bot))  # Add greetings cog
    await bot.add_cog(Valorant(bot))  # Add valorant cog

    utils.botLog("Beep-bop! K1-B0 is ready to roll!")  # Print ready message

    utils.print_line()

    change_status.start()  # Start status loop
    utils.botLog("Started status loop.")


@tasks.loop(minutes=30)
async def change_status():
    """Updates the bot's status every 30 minutes"""
    now = datetime.datetime.now()  # Get time
    status = "Wingman do stuff"  # Set default status

    hour = now.hour + 2  # Get hour
    if hour >= 24: # If hour is greater than 24, subtract 24
        hour -= 24  

    # Set status
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
        status = "Wingman sleep deeply"

    # Change status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))


# -----------------------------------------------------------------------------
# Run K1-B0
bot.run("MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU")
