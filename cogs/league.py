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
ENDPIONT_MATCHES = ["/lol/match/v5/matches/by-puuid/", "/ids"]
ENDPIONT_MATCH = "/lol/match/v5/matches/"

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
    
        try:
            data_summoner = requests.get(request_summoner, timeout=5)
        except requests.exceptions.Timeout:
            await ctx.send(MSG_ERROR_TIMEOUT)
        
        data_summoner = data_summoner.json()
        
        try:
            status_code = data_summoner["status"]["status_code"]
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
        request_matches = URL_API_REGION + ENDPIONT_MATCHES[0] + summoner_puuid + ENDPIONT_MATCHES[1] + "?api_key=" + RIOT_API_KEY
        request_match_count = 5
        
        try:
            data_matches = requests.get(request_matches + "&count=" + str(request_match_count), timeout=5)
        except requests.exceptions.Timeout:
            await ctx.send(MSG_ERROR_TIMEOUT)
            return
        
        data_matches = data_matches.json()
        matches = []
        
        for match_id in data_matches:
            match = LeaugeMatch(ctx, match_id)
            await match.get_match_data()
            matches.append(match)

        print(matches)


class LeaugeMatch:
    """A League of Legends match."""
    def __init__(self, context, match_id):
        self.match_id = match_id
    
    async def get_match_data(self):
        """Retrieves and saves the match information."""
        request_match = URL_API_REGION + ENDPIONT_MATCH + self.match_id + "?api_key=" + RIOT_API_KEY
        data_match = None
        
        try:
            data_match = requests.get(request_match, timeout=5)
        except requests.exceptions.Timeout:
            await self.context.send(MSG_ERROR_TIMEOUT)
            return
