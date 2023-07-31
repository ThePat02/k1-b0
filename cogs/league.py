"""A suite of League of Legends-releated commands."""

import discord
import discord.ext.commands as commands

import requests

MSG_ERROR_TIMEOUT = "The request timed out. Please try again later."
MSG_ERROR_GENERIC = "Something went wrong."

RIOT_API_KEY = "RGAPI-ae6c3b54-c6b4-442e-831e-e0da22e35b8c"

URL_API = "https://euw1.api.riotgames.com"
URL_API_REGION = "https://europe.api.riotgames.com"
ENDPOINT_SUMMONER = "/lol/summoner/v4/summoners/by-name/"
ENDPOINT_MATCHES = ["/lol/match/v5/matches/by-puuid/", "/ids"]
ENDPOINT_MATCH = "/lol/match/v5/matches/"

URL_API_ICON = ["http://ddragon.leagueoflegends.com/cdn/10.15.1/img/profileicon/", ".png"]

class League(commands.Cog):
    """League cog for the bot."""
    def __init__(self, bot):
        self.bot = bot
        print("League cog loaded.")

    @commands.command("lol")
    async def get_user(self, ctx, *, summoner_name):
        """Retrieves and displays the League of Legends profile information of the specified user."""

        # Get summoner information
        request_summoner = URL_API + ENDPOINT_SUMMONER + summoner_name + "?api_key=" + RIOT_API_KEY
        data_summoner = None

        # Try to get summoner information
        try:
            data_summoner = requests.get(request_summoner, timeout=5)
        except requests.exceptions.Timeout:
            await ctx.send(MSG_ERROR_TIMEOUT)

        # Convert response to JSON
        data_summoner = data_summoner.json()
        
        # Check if the response is valid 
        try:
            # If status_code is present, the request failed
            # If status_code is not present, the request succeeded
            data_summoner["status"]["status_code"]

            # TODO: Implement other errors

            await ctx.send(MSG_ERROR_GENERIC)
            return
        except KeyError:
            pass

        # Save summoner information
        summoner_name = data_summoner["name"]
        summoner_puuid = data_summoner["puuid"]
        summoner_icon = data_summoner["profileIconId"]
        summoner_level = data_summoner["summonerLevel"]

        # Get match history
        data_matches = None
        request_matches = URL_API_REGION + ENDPOINT_MATCHES[0] + summoner_puuid + ENDPOINT_MATCHES[1] + "?api_key=" + RIOT_API_KEY
        request_match_count = 5

        # Try to get match history
        try:
            data_matches = requests.get(request_matches + "&count=" + str(request_match_count), timeout=5)
        except requests.exceptions.Timeout:
            await ctx.send(MSG_ERROR_TIMEOUT)
            return

        # Convert response to JSON
        data_matches = data_matches.json()

        # Fill matches list with match objects   
        matches = []
        for match_id in data_matches:
            match = LeaugeMatch(ctx, summoner_puuid, match_id) # Create match object
            await match.get_match_data()       # Fill match object with data
            matches.append(match)              # Add match object to list


class LeaugeMatch:
    """A League of Legends match, containing all relevant information."""
    def __init__(self, context, summoner_puuid, match_id):
        self.summoner_puuid = summoner_puuid
        self.context = context
        self.match_id = match_id

        # Match information
        self.game_mode = "Unknown"
        self.has_won = "None"
        self.champion = "None"
        self.kda = [0, 0, 0]

    async def get_match_data(self):
        """Retrieves and saves the match information."""
        request_match = URL_API_REGION + ENDPOINT_MATCH + self.match_id + "?api_key=" + RIOT_API_KEY
        data_match = None

        try:
            data_match = requests.get(request_match, timeout=5)
        except requests.exceptions.Timeout:
            await self.context.send(MSG_ERROR_TIMEOUT)
            return

        data_match = data_match.json() # Convert response to JSON

        # Match participants to summoner
        for participant in data_match["info"]["participants"]:
            if participant["puuid"] == self.summoner_puuid:
                self.has_won = participant["win"]
                if self.has_won:
                    self.has_won = "Victory"
                else:
                    self.has_won = "Defeat"

                self.champion = participant["championName"]
                self.kda = [participant["kills"], participant["deaths"], participant["assists"]]

        # Determine game mode
        queue_id = data_match["info"]["queueId"] # Get queue ID
        match queue_id:
            case 420:
                self.game_mode = "Ranked Solo/Duo"
            case 440:
                self.game_mode = "Ranked Flex"
            case 430:
                self.game_mode = "Normal Blind Pick"
            case 400:
                self.game_mode = "Normal Draft Pick"
            case 450:
                self.game_mode = "ARAM"
            case _:
                self.game_mode = "Event"
