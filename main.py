import discord
from discord.ext import commands
import logging
import os
import asyncio
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
intents.presences = True
intents.guilds = True
intents.moderation = True

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.tree.sync()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do this!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: `{error.param.name}`")
    elif isinstance(error, commands.CommandNotFound):
        pass

async def main():
    discord.utils.setup_logging(handler=handler, level=logging.DEBUG)
    async with bot:
        for cogs in ["cogs.info", "cogs.moderation", "cogs.fun"]:
            await bot.load_extension(cogs)
        await bot.start(token)

asyncio.run(main())