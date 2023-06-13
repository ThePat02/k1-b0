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
        moviedb = imdb.Cinemagoer() # Create imdb object

        result_movies = moviedb.search_movie(movie_query) # Search for movie
        top_result = result_movies[0] # Get top result

        movie = moviedb.get_movie(top_result.movieID) # Get movie data
        
        title = movie["title"]
        year = movie["year"]
        cover = movie["cover url"]
        plot = movie["plot"]
        rating = movie["rating"]
        runtimes = movie["runtimes"]
        
        genres = movie["genres"]
        output_genres = ""
        for genre in genres:
            if output_genres != "":
                output_genres += ", " + genre
            else:
                output_genres += genre
        
        languages = movie["languages"]
        output_languages = ""
        for language in languages:
            if output_languages != "":
                output_languages += ", " + language
            else:
                output_languages += language
        
        directors = movie["director"]
        output_directors = ""
        for director in directors:
            if output_directors != "":
                output_directors += ", " + director["name"]
            else:
                output_directors += director["name"]
        
        writers = movie["writer"]
        output_writers = ""
        for writer in writers:
            if output_writers != "":
                output_writers += ", " + writer["name"]
            else:
                output_writers += writer["name"]
        
        cast = movie["cast"]

        embed = discord.Embed(title=title,
                            description=str(year) + " - " + runtimes[0] + " - " + str(rating) + " ⭐\n\nDirected by " +
                            output_directors + "\nWritten by " + output_writers,
                            colour=0xffd500)

        embed.set_author(name="Internet Movie Database")

        embed.add_field(name="Plot",
                        value=plot[0], inline=False)
        embed.add_field(name="Cast",
                        value="Tom, TOm, THom", inline=False)
        embed.add_field(name="Genres",
                        value=output_genres, inline=False)
        embed.add_field(name="Languages",
                        value=output_languages, inline=False)
        embed.add_field(name="Links",
                        value="TODO imbd usw", inline=False)

        embed.set_thumbnail(url=cover)

        embed.set_footer(text="❤️ Keebos IMDB Search")

        await ctx.send(embed=embed)
    
