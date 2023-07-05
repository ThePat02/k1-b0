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
        message_loading = await ctx.send("I'm scanning the archives...")
        await message_loading.add_reaction("🎥")
        await message_loading.add_reaction("🎞️")
        await message_loading.add_reaction("📺")
        await message_loading.add_reaction("💃")

        moviedb = imdb.Cinemagoer() # Create imdb object

        result_movies = moviedb.search_movie(movie_query) # Search for movie

        try:
            # Try to get top result
            top_result = result_movies[0] 
        except IndexError:
            # If no results found
            await message_loading.delete()
            await ctx.send("I couldn't find any movies with that name. Impossible! The archives must be incomplete.")      
            return    

        movie = moviedb.get_movie(top_result.movieID) # Get movie data

        imdb_url = moviedb.get_imdbURL(movie)

        title = movie["title"]
        year = movie["year"]

        cover = None
        if "cover url" in movie:
            cover = movie["cover url"]

        plot = "N/A"
        if "plot" in movie:
            plot = movie["plot"]

        rating = "No rating found."
        if "rating" in movie:
            rating = movie["rating"]

        runtime = movie["runtimes"][0]
        output_runtime = str(runtime) + " minutes"

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
            if not "name" in director:
                continue

            if output_directors != "":
                output_directors += ", " + director["name"]
            else:
                output_directors += director["name"]

        writers = movie["writer"]
        output_writers = ""
        for writer in writers:
            # if writer has key name
            if not "name" in writer:
                continue

            if output_writers != "":
                output_writers += ", " + writer["name"]
            else:
                output_writers += writer["name"]

        cast = movie["cast"]
        output_cast = ""
        max_cast = 5
        cast_count = 0
        for actor in cast:
            if cast_count >= max_cast:
                break

            if not "name" in actor:
                continue

            if output_cast != "":
                output_cast += ", " + actor["name"]
            else:
                output_cast += actor["name"]
            cast_count += 1

        embed = discord.Embed(title=title + " - " + str(rating) + " / 10 ⭐",
                            description="\nDirected by " +
                            output_directors + "\nWritten by " + output_writers,
                            colour=0xffd500)

        embed.set_author(name=str(year) + " - " + output_runtime)

        embed.add_field(name="Plot",
                        value=plot[0], inline=False)
        embed.add_field(name="Cast",
                        value=output_cast, inline=False)
        embed.add_field(name="Genres",
                        value=output_genres, inline=False)
        embed.add_field(name="Languages",
                        value=output_languages, inline=False)
        embed.add_field(name="Links",
                        value="[Open on IMDb](" + imdb_url + ")", inline=False)

        embed.set_thumbnail(url=cover)

        embed.set_footer(text="❤️ Keebos IMDb Search")

        await message_loading.delete()
        await ctx.send(embed=embed)
