import discord
from data.database import Database
from discord.ext import commands


""" 
To anyone that wants to edit this, remeber:
result[0] = title
result[1] = description
result[2] = author
result[3] = lock (int boolean)
"""

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

    @snippet.command(aliases = ["a"])
    async def add(self, ctx, title, *, description):
        author = ctx.author.id
        locked = 0
        if await self.bot.db.get_one("snippets", "title", title) is not None:
            await ctx.send("This snippet already exists! ")
            return
        else:
            await self.bot.db.insert("snippets", (title, description, author, locked))
            await ctx.send(f"Snippet {title} created! ")
            

    @snippet.command(aliases = ["e"])
    async def edit(self, ctx, title, *, description):
        result = await self.bot.db.get_one("snippets", "title", title)
        if result is None:
            await ctx.send("Snippet not found. ")
            return
        elif result[3] == 1:
            await ctx.send("This snippet is closed. Ask a moderator to unlock if you want to edit it. ")
            return
        else:
            if result[2] == ctx.author.id:
                await self.bot.db.update("snippets", "description", description, "title", title)
                await ctx.send(f"Snippet {title} updated succesfully.")
            else: await ctx.send("This snippet is not yours. Ask the author if you want to edit it.")

    @snippet.command(aliases = ["d"])
    async def delete(self, ctx, title):
        result = await self.bot.db.get_one("snippets", "title", title)
        if result is None:
            await ctx.send("Snippet not found. ")
            return
        elif result[2] == ctx.author.id:
            await self.bot.db.delete("snippets", "title", title)
            await ctx.send(f"Snippet {title} deleted succesfully. ")
            return
        elif ctx.author.guild_permissions.manage_messages:
            await self.bot.db.delete("snippets", "title", title)
            await ctx.send(f"Snippet {title} deleted succesfully. ")
        else:
            await ctx.send(f"You're not the author of {title} and don't have permission to do this. ")
 

    @snippet.command(aliases = ["lo"])
    @commands.has_permissions(manage_messages = True)
    async def lock(self, ctx, title: str):
        pass

    @snippet.command(aliases = ["ul"])
    @commands.has_permissions(manage_messages = True)
    async def unlock(self, ctx, title: str):
        pass

    @snippet.command(name = "list", aliases = ["l"])
    async def snippet_list(self, ctx, title: str):
        pass

    @snippet.command(aliases = ["b"])
    @commands.has_permissions(moderate_members = True)
    async def ban(self, ctx, user: discord.Member):
        pass

    @snippet.command(aliases = ["ub"])
    @commands.has_permissions(moderate_members = True)
    async def unban(self, ctx, user: discord.Member):
        pass

    @snippet.command(aliases = ["au"])
    async def author(self, ctx, user: discord.Member):
        pass





async def setup(bot):
    await bot.add_cog(Snippets(bot))
