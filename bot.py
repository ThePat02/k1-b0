import discord
from discord.ext import commands

import requests
import json

COMMAND_PREFIX = '?'
URL = "https://api.henrikdev.xyz/valorant/v1/"
URL_MATCH = "https://api.henrikdev.xyz/valorant/v3/matches/eu/"

COLOR_VALO = 0xfe3939
COLOR_VICTORY = 0x00ff00
COLOR_DEFEAT = 0xff0000

intents = discord.Intents.default()
intents.message_content = True

class ValorantUser:
    """A valornt user object that contains the user's information"""
    def __init__(self, name, tag, card, level):
        self.name = name
        self.tag = tag
        self.card = card
        self.level = level

class ValorantMatch:
    """A valorant match object that contains the match's information"""
    def __init__(self, location, mode, team, result):
        self.location = location
        self.mode = mode
        self.team = team
        self.result = result

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.command()
async def valo(ctx, user):
    """TODO WRITE DOCSTRING"""
    
    #Split the user by the # to get the username and discriminator
    user = user.split('#')
    username = user[0]
    discriminator = user[1]
    
    # Get the user's information
    response_user = requests.get(URL + "account/" + username + "/" + discriminator)
    response_user = response_user.json()
    
    player = ValorantUser(response_user['data']['name'], response_user['data']['tag'], response_user['data']['card']['small'], response_user['data']['account_level'])
    
    # Print the user's information
    embed=discord.Embed(title="Keebos Valorant Tracker", color=COLOR_VALO)
    embed.set_thumbnail(url=player.card)
    embed.add_field(name=player.name + "#" + player.tag, value="Level " + str(player.level), inline=True)
    await ctx.send(embed=embed)
    
    # Get the users match history
    response_match = requests.get(URL_MATCH + username + "/" + discriminator)
    response_match = response_match.json()
    
    for match in response_match['data']:
        team = ""
        character = ""
        portrait = ""
        stats = [0, 0, 0]
        result = "Defeat"
        color = COLOR_DEFEAT
        round = [0, 0]
        
        for player in match['players']['all_players']:
            if player['name'] == username and player['tag'] == discriminator:
                team = player['team']
                character = player['character']
                stats[0] = player['stats']['kills']
                stats[1] = player['stats']['deaths']
                stats[2] = player['stats']['assists']
                portrait = player['assets']['agent']['small']
                
        if match['teams'][team.lower()]['has_won'] == True:
            result = "Victory"
            color = COLOR_VICTORY
        
        round = [match['teams'][team.lower()]['rounds_won'], match['teams'][team.lower()]['rounds_lost']]
                    
                        
        new_match = ValorantMatch(match['metadata']['map'],
                                  match['metadata']['mode'],
                                  team,
                                  result)
        
        embed = discord.Embed(title=result + f" - {round[0]} / {round[1]}",
                      colour=color)

        embed.set_author(name=new_match.location + " - " + new_match.mode)

        embed.set_footer(text=character + f"  -  {stats[0]} / {stats[1]} / {stats[2]}",
                        icon_url=portrait)

        await ctx.send(embed=embed)
    

bot.run('MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU')
