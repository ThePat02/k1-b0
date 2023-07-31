"""Essentials cog for the bot."""

import discord
import discord.ext.commands as commands

class Essentials(commands.Cog):
    """Essentials cog for the bot."""
    def __init__(self, bot):
        self.bot = bot
        print("Essentials cog loaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends a welcome message when a member joins the server."""
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome to Antarctica, {member.mention}. I am K1-B0, the Ultimate Robot!')

    @commands.command()
    async def help(self, ctx):
        """Sends information about the bot's commands."""
        embed = discord.Embed(title="Keebo, The Ultimate Robot",
                            description="I am K1-B0, the Ultimate Robot, but you can call me Keebo. I have several commands that will make your life easier.",
                            colour=0x00b0f4)

        embed.set_author(name="K1-B0")

        embed.add_field(name="Essentials",
                        value="`?help`:\nShows a list of my available commands.", inline=False)
        
        embed.add_field(name="Valorant",
                        value="`?valo <Username#Tag>`:\nRetrieves and displays the Valorant profile information and the most recent matches of the specified user.\n\n`?valo @DiscordUser`:\nRetrieves and displays the Valorant profile information and the most recent matches of the Discord user, provided they have linked their Riot-ID.\n\n`?link <Username#Tag>`:\nEstablishes a connection between your Riot-ID and Discord-ID. If the link already exists, it will update the associated ID.\n\n`?unlink`:\nRemoves the link between your Discord-ID and the associated Riot-ID.", inline=False)

        embed.add_field(name="League of Legends",
                        value="`?lol <Username>`:\nRetrieves and displays the profile information and the most recent matches of the specified user. (EUW users only)", inline=False)

        embed.add_field(name="Cinema",
                        value="`?movie <Movie Name>`:\nRetrieves and displays information about the specified movie from IMDb.")

        await ctx.send(embed=embed)
