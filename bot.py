import discord
from discord.ext import commands

import requests
import json

COMMAND_PREFIX = '?'
URL = "https://api.henrikdev.xyz/valorant/v1/"

intents = discord.Intents.default()
intents.message_content = True

class ValorantUser:
    """A valornt user object that contains the user's information"""
    def __init__(self, name, tag, card, level):
        self.name = name
        self.tag = tag
        self.card = card
        self.level = level

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.command()
async def valo(ctx, user):
    """TODO WRITE DOCSTRING"""
    
    #Split the user by the # to get the username and discriminator
    user = user.split('#')
    username = user[0]
    discriminator = user[1]
    
    response_user = requests.get(URL + "account/" + username + "/" + discriminator)
    response_user = response_user.json()
    
    player = ValorantUser(response_user['data']['name'], response_user['data']['tag'], response_user['data']['card']['small'], response_user['data']['account_level'])
    
    await ctx.send(player.name + "#" + player.tag +  " Level " + str(player.level))
    await ctx.send(player.card)
    

bot.run('MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU')
