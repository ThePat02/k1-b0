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
ENDPOINT_LEAGUE = "/lol/league/v4/entries/by-summoner/"

URL_DDRAGON_VERSION = "https://ddragon.leagueoflegends.com/api/versions.json"
CURRENT_VERSION = "13.14.1" # Define fallback version

# Try to get current version
try:
    CURRENT_VERSION = requests.get(URL_DDRAGON_VERSION, timeout=5)
    CURRENT_VERSION = CURRENT_VERSION.json()[0]
except requests.exceptions.Timeout:
    print(MSG_ERROR_TIMEOUT)

URL_API_ICON = ["http://ddragon.leagueoflegends.com/cdn/" + CURRENT_VERSION + "/img/profileicon/", ".png"]

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
            # pylint: disable=pointless-statement
            data_summoner["status"]["status_code"]

            # TODO: Implement other errors

            await ctx.send(MSG_ERROR_GENERIC)
            return
        except KeyError:
            pass

        # Save summoner information
        summoner_name = data_summoner["name"]
        summoner_puuid = data_summoner["puuid"]
        summoner_id = data_summoner["id"]
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

        request_league = URL_API + ENDPOINT_LEAGUE + summoner_id + "?api_key=" + RIOT_API_KEY

        # Try to get ranks
        try:
            data_league = requests.get(request_league, timeout=5)
        except requests.exceptions.Timeout:
            await ctx.send(MSG_ERROR_TIMEOUT)
            return

        data_league = data_league.json() # Convert response to JSON

        result_league = ""
        for league in data_league:
            queue_type = league["queueType"]
            match queue_type:
                case "RANKED_SOLO_5x5":
                    queue_type = "Ranked Solo/Duo"
                case "RANKED_FLEX_SR":
                    queue_type = "Ranked Flex"
                case _:
                    continue

            wins = league["wins"]
            losses = league["losses"]
            league_points = league["leaguePoints"]

            tier = league["tier"]
            rank = league["rank"]

            result = tier + " " + rank + " (" + str(league_points) + " LP) • " + str(wins) + "W/" + str(losses) + "L (" + queue_type + ")\n"
            result_league += result

        embed = discord.Embed(title=summoner_name + " • Level " + str(summoner_level),
                            description=result_league,
                            colour=0x091428)

        embed.set_author(name="League of Legends",
                        icon_url="https://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/1052.png")

        for match in matches:
            embed.add_field(name=match.has_won + " " + match.game_mode,
                            value= match.champion + " (" + str(match.kda[0]) + "/" + str(match.kda[1]) + "/" + str(match.kda[2]) + ") " + match.lane, inline=False)


        url_tracker = "https://www.op.gg/summoners/euw/" + summoner_name.replace(" ", "%20")

        embed.add_field(name="Links",
                        value="[OP.gg](" + url_tracker + ")", inline=False)

        # Set the summoner icon
        embed.set_thumbnail(url=URL_API_ICON[0] + str(summoner_icon) + URL_API_ICON[1])

        # Set the footer
        embed.set_footer(text="❤️ Keebos League Tracker")

        await ctx.send(embed=embed)


class LeaugeMatch:
    """A League of Legends match, containing all relevant information."""
    def __init__(self, context, summoner_puuid, match_id):
        self.summoner_puuid = summoner_puuid
        self.context = context
        self.match_id = match_id

        # Match information
        self.duration = 0
        self.game_mode = "Unknown"
        self.has_won = "Unknown"
        self.champion = "Unknown"
        self.lane = "Unknown"
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
                    self.has_won = "🟩"
                else:
                    self.has_won = "🟥"

                self.duration = data_match["info"]["gameDuration"]
                if self.duration < 240:
                    self.has_won = "⬜ Remake -"

                self.champion = participant["championName"]

                self.lane = participant["teamPosition"]
                match self.lane:
                    case "TOP":
                        self.lane = "Top"
                    case "JUNGLE":
                        self.lane = "Jungle"
                    case "MIDDLE":
                        self.lane = "Mid"
                    case "BOTTOM":
                        self.lane = "Bot"
                    case "UTILITY":
                        self.lane = "Support"
                    case _:
                        self.lane = ""

                self.kda = [participant["kills"], participant["deaths"], participant["assists"]]

        # Determine game mode
        queue_id = data_match["info"]["queueId"] # Get queue ID
        match queue_id:
            case 420:
                self.game_mode = "Ranked Solo/Duo 🏆"
            case 440:
                self.game_mode = "Ranked Flex 🏆"
            case 430:
                self.game_mode = "Normal Blind Pick 🎈"
            case 400:
                self.game_mode = "Normal Draft Pick 🎈"
            case 450:
                self.game_mode = "ARAM 🎲"
            case 0:
                self.game_mode = "Custom 🛠️"
            case _:
                self.game_mode = "Event 🎉"
