
# This example requires the 'message_content' intent.

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    wait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Wingman eat your brains"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "r6" in message.content.lower():
        await message.channel.send('No.')

client.run('MTA1NzQzMTUxNzI1MDQ3Mzk5NA.GF8Piy.0d85mzmOqE6rPd0YcZLNQeJysjaiLXz1wB2MgU')
