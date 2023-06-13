"""A suite of Valorant-related commands for Keebo"""

import discord
import discord.ext.commands as commands
import requests

import mysql.connector


API_URL = "https://api.henrikdev.xyz/valorant/v1/"
API_URL_MATCH = "https://api.henrikdev.xyz/valorant/v3/matches/eu/"


def db_connect():
    """Connects to the database"""
    cnx = mysql.connector.connect(
        host='db-eu-02.sparkedhost.us',
        port=3306,
        user='u96181_SlSwXhCZ2F',
        password='XMK3v1aO!sq==CXaEMl+.ufz',
        database='s96181_KeebosBrain'
    )
    return cnx


def db_add_user(discord_id, valorant_id):
    """Adds a user to the database"""
    # Connect to the database
    cnx = db_connect()
    
    cursor = cnx.cursor() # Create a cursor

    # Define the query
    insert_query = """
        INSERT INTO valorant_users (discord, valorant)
        VALUES (%s, %s)
    """
    entry_data = (discord_id, valorant_id)

    cursor.execute(insert_query, entry_data) # Execute the query
    cnx.commit() # Commit the changes
      
    cursor.close() # Close the cursor
    cnx.close() # Close the connection


def db_remove_user(discord_id):
    """Removes a user from the database"""
    # Connect to the database
    cnx = db_connect()
    
    cursor = cnx.cursor() # Create a cursor
    
    # Define the query
    delete_query = """
        DELETE FROM valorant_users
        WHERE discord = %s
    """
    entry_data = (discord_id,)

    cursor.execute(delete_query, entry_data) # Execute the query
    cnx.commit() # Commit the changes
    
    cursor.close() # Close the cursor
    cnx.close() # Close the connection


def db_get_user_valorant(discord_id):
    """Gets a user's Valorant ID from the database"""
    # Connect to the database
    cnx = db_connect()
    
    cursor = cnx.cursor() # Create a cursor
    
    # Trim discord ID
    discord_id = discord_id.replace("<", "")
    discord_id = discord_id.replace(">", "")
    discord_id = discord_id.replace("@", "")
    
    # Define the query
    select_query = """
        SELECT valorant
        FROM valorant_users
        WHERE discord = %s
    """
    entry_data = (discord_id,)

    cursor.execute(select_query, entry_data) # Execute the query
    result = cursor.fetchone() # Get the result
    
    cursor.close() # Close the cursor
    cnx.close() # Close the connection

    return result[0]


def db_user_exists(discord_id) -> bool:
    """Checks if a user exists in the database"""
    # Connect to the database
    cnx = db_connect()
    
    cursor = cnx.cursor() # Create a cursor
    
    # Define the query
    select_query = """
        SELECT COUNT(*)
        FROM valorant_users
        WHERE discord = %s
    """
    entry_data = (discord_id,)

    cursor.execute(select_query, entry_data) # Execute the query
    result = cursor.fetchone() # Get the result
    
    cursor.close() # Close the cursor
    cnx.close() # Close the connection

    return result[0] > 0


class Valorant(commands.Cog):
    """A suite of Valorant-related commands for Keebo"""

    def __init__(self, bot):
        self.bot = bot
        print("Valorant cog loaded.")

    @commands.command()
    async def link(self, ctx, valorant_id):
        """Links a user's Discord account to their Valorant account"""
        if not db_user_exists(ctx.author.id):
            db_add_user(ctx.author.id, valorant_id)
            await ctx.send("I've linked your Discord account to your Valorant account. ^^")
        else:
            db_remove_user(ctx.author.id)
            db_add_user(ctx.author.id, valorant_id)
            await ctx.send("I have updated your Valorant account. ^^")

    @commands.command()
    async def unlink(self, ctx):
        """Unlinks a user's Discord account from their Valorant account"""
        if db_user_exists(ctx.author.id):
            db_remove_user(ctx.author.id)
            await ctx.send("I've unlinked your Discord account from your Valorant account. :(")
        else:
            await ctx.send("You don't have a Valorant account linked to your Discord account. :/")

    @commands.command()
    async def valo(self, ctx, user):
        """Fetches the user's Valorant information and displays it"""
        if user.startswith("<@") and user.endswith(">"):
            user = user[2:-1] # Trim the first 2 and last 1 characters

            if not db_user_exists(user):
                await ctx.send("That user doesn't have a Valorant account linked to their Discord account. Use `?link <name#tag>` to change that!")
                return
            user = db_get_user_valorant(user)
        
        user = user.split("#")  # Split the user by the hashtag
        user[0] = user[0].replace(" ", "%20")  # Replace blank spaces with %20

        # Get the user's information
        try:
            user_info = requests.get(
                API_URL + "account/" + user[0] + "/" + user[1], timeout=10
            )
        except IndexError:
            await ctx.send("Ouch. I think your input isn't a valid username...")
            return
        except requests.exceptions.Timeout:
            await ctx.send("The Servers are taking too long to respond. :/")
            return

        # Handle response codes
        if user_info.status_code == 404:
            await ctx.send("Looks like that user doesn't exist. :/")
            return
        elif user_info.status_code != 200:
            await ctx.send("Something went wrong. Not exactly sure what, though. :/")
            return

        try:
            user_mmr = requests.get(
                API_URL + "mmr/eu" + "/" + user[0] + "/" + user[1], timeout=10
            )
            last_matches = requests.get(API_URL_MATCH + user[0] + "/" + user[1], timeout=10)
        except requests.exceptions.Timeout:
            ctx.send("The Servers are taking too long to respond. :/")
            return

        # Convert the response to JSON
        user_info = user_info.json()
        user_mmr = user_mmr.json()
        last_matches = last_matches.json()
        
        # Redefine username
        user[0] = user_info["data"]["name"]
        user[1] = user_info["data"]["tag"]

        user[0] = user[0].replace("%20", " ")  # Replace %20 with blank spaces again

        # Setup user information
        username = user_info["data"]["name"] + "#" + user_info["data"]["tag"]
        card = user_info["data"]["card"]["small"]
        level = user_info["data"]["account_level"]
        rank = "Unranked"
        rank_badge = ""
        rank_points = ""
        if user_mmr["data"]["currenttierpatched"] is not None:
            rank = user_mmr["data"]["currenttierpatched"]
            rank_badge = user_mmr["data"]["images"]["small"]

            rank_points = user_mmr["data"]["ranking_in_tier"]
            rank_points_counter = rank_points
            rank_points = " • " + str(rank_points) + " / 100 • ["
            for i in range(0, 100, 10):
                if i > rank_points_counter:
                    rank_points += "-"
                else:
                    rank_points += "+"
            rank_points += "]"

        # Setup embed
        embed = discord.Embed(
            title=username + "  •  Level " + str(level), description="", colour=0xFE3939
        )

        embed.set_author(name=rank + rank_points, icon_url=rank_badge)

        for match in last_matches["data"]:
            match_map = match["metadata"]["map"]
            match_mode = match["metadata"]["mode"]
            match_icon = "🎮"
            result_icon = "🟪"
            if match_mode == "Deathmatch":
                match_icon = "🔫"
            if match_mode == "Spike Rush":
                match_icon = "🔥"
            if match_mode == "Competitive":
                match_icon = "🏆"
            if match_mode == "Unrated":
                match_icon = "🎈"
            if match_mode == "Swiftplay":
                match_icon = "⏱️"
            match_timestamp = match["metadata"]["game_start_patched"]

            match_character = ""
            match_team = ""
            match_stats = [0, 0, 0]
            match_shots = [0, 0, 0]

            match_rounds_won = 0
            match_rounds_lost = 0

            for player in match["players"]["all_players"]:
                if player["name"] == user[0] and player["tag"] == user[1]:
                    match_character = player["character"]
                    match_team = player["team"].lower()
                    match_stats = [
                        player["stats"]["kills"],
                        player["stats"]["deaths"],
                        player["stats"]["assists"],
                    ]
                    match_shots = [
                        player["stats"]["bodyshots"],
                        player["stats"]["headshots"],
                        player["stats"]["legshots"],
                    ]

            match_hits = match_shots[0] + match_shots[1] + match_shots[2]
            match_hs_rate = 0
            if match_hits > 0:
                match_hs_rate = round(match_shots[1] / match_hits * 100, 2)
            content_hs_rate = ""
            if match_mode != "Deathmatch":
                content_hs_rate = f" • {match_hs_rate}% HS"

            match_rounds_won = 0
            match_rounds_lost = 0
            has_won = False

            rounds_won_string = ""

            if match_mode != "Deathmatch":
                match_rounds_won = match["teams"][match_team]["rounds_won"]
                match_rounds_lost = match["teams"][match_team]["rounds_lost"]
                has_won = match["teams"][match_team]["has_won"]
                rounds_won_string = (
                    "  |  " + str(match_rounds_won) + " - " + str(match_rounds_lost)
                )
                if has_won:
                    result_icon = "🟩"
                else:
                    result_icon = "🟥"

            embed.add_field(
                name=result_icon
                + "  "
                + match_mode
                + "  "
                + match_icon
                + rounds_won_string
                + "  |  "
                + match_map,
                value=match_character
                + f" ({match_stats[0]}/{match_stats[1]}/{match_stats[2]})"
                + content_hs_rate
                + "\n"
                + match_timestamp,
                inline=False,
            )  # Add the match field

        user[0] = user[0].replace(" ", "%20")  # Replace blank spaces with %20 again
        tracker_url = (
            "https://tracker.gg/valorant/profile/riot/"
            + user[0]
            + "%23"
            + user[1]
            + "/overview"
        )

        embed.add_field(
            name="Links", value=f"[Tracker.gg]({tracker_url})", inline=False
        )  # Add the links field

        embed.set_thumbnail(url=card)  # Set the thumbnail
        embed.set_footer(text="❤️ Keebos Valorant Tracker")  # Set the footer

        await ctx.send(embed=embed)  # Send the embed
