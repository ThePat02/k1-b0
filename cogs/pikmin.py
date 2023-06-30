"""A simple Discord-Based game to celebrate the release of Pikmin 4"""

import discord
import discord.ext.commands as commands

class Pikmin(commands.Cog):
    """Pikmin cog for the bot."""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Pikmin cog loaded.")
