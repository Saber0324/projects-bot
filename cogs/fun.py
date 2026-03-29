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
    async def hog(self,ctx):
        await ctx.send("All hail the supreme leader")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

async def setup(bot):
    await bot.add_cog(Fun(bot))