"""K1-B0 is a discord bot inspired by the character from Danganronpa 3"""

# -----------------------------------------------------------------------------
# Imports

# Import discord library
import discord
from discord.ext import commands, tasks

# Import cogs
from cogs.essentials import Essentials
from cogs.valorant import Valorant
from cogs.cinema import Cinema

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

    bot.remove_command("help") # Remove default help command

    await bot.add_cog(Essentials(bot))  # Add greetings cog
    await bot.add_cog(Valorant(bot))  # Add valorant cog
    await bot.add_cog(Cinema(bot))  # Add cinema cog

    utils.botLog("Beep-bop! K1-B0 is ready to roll!")  # Print ready message

    utils.print_line()

    change_status.start()  # Start status loop


@tasks.loop(minutes=30)
async def change_status():
    """Updates the bot's random status every 30 minutes"""
    activity_type = discord.ActivityType.watching # Set default activity type
    status = "Wingman do stuff"  # Set default status

    # Random status
    status_id = utils.random_number(0, 5)

    if status_id == 0:
        activity_type = discord.ActivityType.listening
        status = "Wingman's inside jokes"
    elif status_id == 1:
        activity_type = discord.ActivityType.watching
        status = "Wingman defuse the spike"
    elif status_id == 2:
        activity_type = discord.ActivityType.playing
        status = "with Wingman"
    elif status_id == 3:
        activity_type = discord.ActivityType.playing
        status = "with Dizzy and Moshpit"
    elif status_id == 4:
        activity_type = discord.ActivityType.watching
        status = "Wingman's dance on TikTok"
    elif status_id == 5:
        activity_type = discord.ActivityType.watching
        status = "Chamber nibble on Wingman"

    await bot.change_presence(activity=discord.Activity(type=activity_type, name=status))
    utils.botLog("Started status loop.")

# -----------------------------------------------------------------------------
# Run K1-B0
bot.run("MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU")
