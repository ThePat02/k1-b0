"""A trivia game, playable on Discord."""

import discord
import discord.ext.commands as commands

import requests
import random
import time

TRIVIA_API_URL = "https://the-trivia-api.com/v2/questions"

class Trivia(commands.Cog):
    """A trivia game, playable on Discord."""
    def __init__(self, bot):
        self.bot = bot
        print("Trivia cog loaded.")
        
    def get_questions(self, category, difficulty, amount):
        """Gets trivia questions from the API."""
        # Build query
        query = TRIVIA_API_URL + "?" + "categories=" + category + "&difficulty=" + difficulty + "&limit=" + amount
        questions = requests.get(query, timeout=60.0).json() # Get questions from API
        return questions
    
    def icon_to_category(self, icon):
        """Converts a reaction icon to a trivia category."""
        category = ""
        if icon == "🎬":
            category = "film_and_tv"
        elif icon == "🎵":
            category = "music"
        elif icon == "🌎":
            category = "geography"
        elif icon == "🧑‍🔬":
            category = "science"
        elif icon == "🏛️":
            category = "history"
        elif icon == "❓":
            category = "general_knowledge"
        
        return category
        
        
    @commands.command("trivia")
    async def start(self, ctx, arg_amount, *, players=""):
        """Starts a trivia game."""
        owner = ctx.message.author
        
        players = players.split(" ")  # Split the players string into a list
        players.append(owner) # Add the owner to the list of players       
        
        # Initialize the scoreboard
        scoreboard = {}
        for player in players:
            scoreboard[player] = 0 
        
        
        message_category = await ctx.send("Choose a trivia category!")
        await message_category.add_reaction("🎬")
        await message_category.add_reaction("🎵")
        await message_category.add_reaction("🌎")
        await message_category.add_reaction("🧑‍🔬")
        await message_category.add_reaction("🏛️")
        await message_category.add_reaction("❓")
        
        def check(reaction, user):
            return user == owner and str(reaction.emoji) in ["🎬", "🎵", "🌎", "🧑‍🔬", "🏛️", "❓"]
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except:
            await message_category.delete()
            await ctx.send("I guess you don't want to play trivia...")
            return
        else:
            await ctx.send('👍')
        
        await message_category.delete()
        
        category = self.icon_to_category(str(reaction.emoji))
        questions = self.get_questions(category, "easy", arg_amount)
        
        for question in questions:
            has_answered = {}
            for player in players:
                has_answered[player] = False
            
            text = question["question"]["text"]
            correct_answer = question["correctAnswer"]
            incorrect_answer_1 = question["incorrectAnswers"][0]
            incorrect_answer_2 = question["incorrectAnswers"][1]
            incorrect_answer_3 = question["incorrectAnswers"][2]
            
            answers = [correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3]
            random.shuffle(answers)
            
            output_answers = ""
            for i in range(len(answers)):
                output_answers += str(i + 1) + ". " + answers[i] + "\n"

            await ctx.send(text)
            message_choices = await ctx.send(output_answers)
            await message_choices.add_reaction("1️⃣")
            await message_choices.add_reaction("2️⃣")
            await message_choices.add_reaction("3️⃣")
            await message_choices.add_reaction("4️⃣")
            
            def check_answer(reaction, user):
                return user in players and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            
            # Wait until all players have answered
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=check_answer) 
                has_answered[user] = True  # Mark the player as having answered
                print(has_answered)
                if False not in has_answered.values():
                    break
