"""Essentials cog for the bot."""

import discord
import discord.ext.commands as commands

import imdb

class Cinema(commands.Cog):
    """Cinema cog for the bot."""
    def __init__(self, bot):
        self.bot = bot
        print("Cinema cog loaded.")


    @commands.command()
    async def movie(self, ctx, *, movie_query):
        """Queries the movie database for a movie"""
        ia = imdb.Cinemagoer() # Create imdb object
        
        result_movies = ia.search_movie(movie_query) # Search for movie
        top_result = result_movies[0] # Get top result
        
        print(result_movies)
