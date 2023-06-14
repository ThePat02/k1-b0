"""A trivia game, playable on Discord."""

import discord
import discord.ext.commands as commands

class Trivia(commands.Cog):
    """A trivia game, playable on Discord."""
    def __init__(self, bot):
        self.bot = bot
        print("Essentials cog loaded.")
