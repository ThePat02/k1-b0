"""Greetings cog for the bot."""

import discord
import discord.ext.commands as commands

class Greetings(commands.Cog):
    """Greetings cog for the bot."""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Greetings cog loaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member
