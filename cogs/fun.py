import random
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, sunshine.")

    @commands.command()
    async def meow(self, ctx):
        await ctx.send("Meow too!")

    @commands.command()
    async def hog(self, ctx):
        await ctx.send("All hail the supreme leader")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, arg):
        await ctx.send(arg)
        
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            content = message.content.lower()
            
            if "is this true?" in content:
                text_responses=["Yes","No","Maybe","Ask Hog"]
                gif_responses=["https://tenor.com/bU4oZ.gif"]
                
                if random.random() < 0.5:
                    await message.reply(random.choice(text_responses))
                else:
                    await message.reply(random.choice(gif_responses))
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Fun(bot))
