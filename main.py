import discord
from discord.ext import commands
import logging
import os
import random
import json
from typing import Optional
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
intents.presences = True
intents.guilds = True

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hey!")

@bot.command()
async def meow(ctx):
    await ctx.send("Meow too!")
    
bot.run(token)