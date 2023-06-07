"""A suite of Valorant-related commands for Keebo"""

import discord
import discord.ext.commands as commands
import requests

API_URL = "https://api.henrikdev.xyz/valorant/v1/"
API_URL_MATCH = "https://api.henrikdev.xyz/valorant/v3/matches/eu/"

class Valorant(commands.Cog):
    """A suite of Valorant-related commands for Keebo"""
    def __init__(self, bot):
        self.bot = bot
        print("Valorant cog loaded.")

    @commands.command()
    async def valo(self, ctx, user):
        """Fetches the user's Valorant information and displays it"""
        user = user.split("#") # Split the user by the hashtag
        user[0] = user[0].replace(" ", "%20") # Replace blank spaces with %20

        # Get the user's information
        user_info = requests.get(
            API_URL + "account/" +
            user[0] +
            "/" +
            user[1],
            timeout=10
        )
        user_mmr = requests.get(
            API_URL + "mmr/eu" +
            "/" +
            user[0] +
            "/" +
            user[1],
            timeout=10
        )
        last_matches = requests.get(
            API_URL_MATCH +
            user[0] +
            "/" +
            user[1],
            timeout=10
        )

        # Convert the response to JSON
        user_info = user_info.json()
        user_mmr = user_mmr.json()
        last_matches = last_matches.json()
        
        user[0] = user[0].replace("%20", " ") # Replace %20 with blank spaces again

        # Setup user information
        username = user_info["data"]["name"] + "#" + user_info["data"]["tag"]
        card = user_info["data"]["card"]["small"]
        level = user_info["data"]["account_level"]
        rank = "Unranked"
        rank_badge = ""
        rank_points = ""
        if user_mmr['data']['currenttierpatched'] is not None:
            rank = user_mmr['data']['currenttierpatched']
            rank_badge = user_mmr['data']['images']['small']
            
            rank_points = user_mmr['data']['ranking_in_tier']
            a = rank_points
            rank_points = " • " + str(rank_points) + " / 100 • ["
            for i in range(0, 100, 10):
                if i > a: rank_points += "-"
                else: rank_points += "+"
            rank_points += "]"
                

        # Setup embed
        embed = discord.Embed(title=username + "  •  Level " + str(level),
                            description="",      
                            colour=0xFE3939)

        embed.set_author(name=rank + rank_points,
                        icon_url=rank_badge)
        
        for match in last_matches["data"]:
            match_map = match["metadata"]["map"]
            match_mode = match["metadata"]["mode"]
            match_icon = "🎮"
            result_icon = "🟪"
            if match_mode == "Deathmatch": match_icon = "🔫"
            if match_mode == "Spike Rush": match_icon = "🔥"
            if match_mode == "Competitive": match_icon = "🏆"
            if match_mode == "Unrated": match_icon = "🎈"
            if match_mode == "Swiftplay": match_icon = "⏱️"
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
                        player["stats"]["assists"]
                    ]
                    match_shots = [
                        player["stats"]["bodyshots"],
                        player["stats"]["headshots"],
                        player["stats"]["legshots"]
                    ]
            
            match_hits = match_shots[0] + match_shots[1] + match_shots[2]
            match_hs_rate = 0
            if match_hits > 0: match_hs_rate = round(match_shots[1] / match_hits * 100, 2)
            content_hs_rate = ""
            if match_mode != "Deathmatch": content_hs_rate = f" • {match_hs_rate}% HS"

            match_rounds_won = 0
            match_rounds_lost = 0
            has_won = False
            
            rounds_won_string = ""

            if match_mode != "Deathmatch":
                match_rounds_won = match['teams'][match_team]['rounds_won']
                match_rounds_lost = match['teams'][match_team]['rounds_lost']
                has_won = match['teams'][match_team]['has_won']
                rounds_won_string = "  |  " + str(match_rounds_won) + " - " + str(match_rounds_lost)
                if has_won: result_icon = "🟩"
                else: result_icon = "🟥"

            embed.add_field(
                name=result_icon + "  " + match_mode + "  " + match_icon + rounds_won_string + "  |  " + match_map,
                value=match_character + f" ({match_stats[0]}/{match_stats[1]}/{match_stats[2]})" + content_hs_rate + "\n" + match_timestamp,
                inline=False
            ) # Add the match field

        user[0] = user[0].replace(" ", "%20") # Replace blank spaces with %20 again
        tracker_url = "https://tracker.gg/valorant/profile/riot/" + user[0] + "%23" + user[1] + "/overview"

        embed.add_field(
                name="Links",
                value=f"[Tracker.gg]({tracker_url})",
                inline=False
        ) # Add the links field

        embed.set_thumbnail(url=card) # Set the thumbnail
        embed.set_footer(text="❤️ Keebos Valorant Tracker") # Set the footer


        await ctx.send(embed=embed) # Send the embed
