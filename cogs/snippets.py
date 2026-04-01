import discord
from data.database import Database
from discord.ext import commands

class Snippets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command = True, aliases = ["s"])
    async def snippet(self, ctx, target: str = None):
        if ctx.invoked_subcommand is None and target is None:    
            await ctx.send("`!help snippet` for more information. ")
            return
        elif target:

            result = await self.bot.db.get_one("snippets", "title", target)
            if result is None:
                await ctx.send("Snippet not found. ")
                return

            message = f"### ***{result[0]}*** \n\n_*{result[1]}*_ \n\n-# — Written by {await self.bot.fetch_user(result[2])}"
            await ctx.send(message)

    @snippet.command(aliases = ["sa"])
    async def add(self, ctx, title, *, description):
        author = ctx.author.id
        locked = 0
        if await self.bot.db.get_one("snippets", "title", title) is not None:
            await ctx.send("This snippet already exists! ")
            return
        else:
            await self.bot.db.insert("snippets", (title, description, author, locked))
            await ctx.send(f"Snippet {title} created! ")
            

    @snippet.command(aliases = ["se"])
    async def edit(self, ctx, title: str):
        pass

    @snippet.command(aliases = ["sd"])
    async def delete(self, ctx, title: str):
        pass

    @snippet.command(aliases = ["slo"])
    @commands.has_permissions(manage_messages = True)
    async def lock(self, ctx, title: str):
        pass

    @snippet.command(aliases = ["sul"])
    @commands.has_permissions(manage_messages = True)
    async def unlock(self, ctx, title: str):
        pass

    @snippet.command(name = "list", aliases = ["sl"])
    async def snippet_list(self, ctx, title: str):
        pass

    @snippet.command(aliases = ["sb"])
    @commands.has_permissions(moderate_members = True)
    async def ban(self, ctx, user: discord.Member):
        pass

    @snippet.command(aliases = ["sub"])
    @commands.has_permissions(moderate_members = True)
    async def unban(self, ctx, user: discord.Member):
        pass

    @snippet.command(aliases = ["sau"])
    async def author(self, ctx, user: discord.Member):
        pass





async def setup(bot):
    await bot.add_cog(Snippets(bot))
