"""A simple Discord-Based game to celebrate the release of Pikmin 4"""

import discord
import discord.ext.commands as commands

import mysql.connector


class Pikmin(commands.Cog):
    """Pikmin cog for the bot."""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Pikmin cog loaded.")

    @commands.command("pikmin")
    async def command_pikmin(self, ctx):
        """Default info command for the Pikmin cog."""
        await ctx.send("A Pikmin-Themed game is coming soon!")
        # TODO: Implement information screen

    @commands.command("camp")
    async def command_user_info(self, ctx):
        """Displays the informations of the user"""
        user = ctx.author


class Database:
    """Simple database implementation."""
    def __init__(self) -> None:
        pass

    def connect(self):
        """Connects to the database"""
        cnx = mysql.connector.connect(
            host='db-eu-02.sparkedhost.us',
            port=3306,
            user='u96181_SlSwXhCZ2F',
            password='XMK3v1aO!sq==CXaEMl+.ufz',
            database='s96181_KeebosBrain'
        )
        return cnx

    def disconnect(self, cnx):
        """Disconnects from the database"""
        cnx.close()

    def query(self, query : str):
        """Queries the database."""
        cnx = self.connect() # Connect to the database
        cursor = cnx.cursor() # Create a cursor

        cursor.execute(query) # Execute the query
        result = cursor.fetchone() # Get the result

        cursor.close() # Close the cursor
        cnx.close() # Close the connection

        return result[0]

    def user_exists(self, user_tag : str) -> bool:
        """Checks if the user exists in the database"""
        query = f"SELECT COUNT(*) FROM pikmin_user_data WHERE user_tag = {user_tag}"
        result = self.query(query) # Query the database
        return result[0] > 0 # Return if the user exists
