import discord
from discord.ext import commands
from data.models import Snippet

class Snippets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_snippet(self, ctx, title):
        result = await self.bot.db.get_one("snippets", "title", title)
        if result is None:
            await ctx.send("Snippet not found. ")
            return
        else:
            snippet = Snippet.from_row(result)
            return snippet



    @commands.group(invoke_without_command = True, aliases = ["s"])
    async def snippet(self, ctx, title: str = None):
        if ctx.invoked_subcommand is None and title is None:    
            await ctx.send("`!help snippet` for more information. ")
            return
        elif title:
            snippet = await self.get_snippet(ctx, title)
            message = f"""## ***{snippet.title}***  \n\n_*{snippet.description}*_    \n\n-# — Written by {await self.bot.fetch_user(snippet.author_id)}   \n\n{"-# — :lock:" if snippet.lock == 1 else ""}"""
            await ctx.send(message)

    @snippet.command(aliases = ["a"])
    async def add(self, ctx, title, *, description):
        author = ctx.author.id
        locked = 0
        snippet = await self.get_snippet(ctx, title)
        if snippet  is not None:
            await ctx.send("This snippet already exists! ")
            return
        else:
            await self.bot.db.insert("snippets", (title, description, author, locked))
            await ctx.send(f"Snippet {title} created! ")
            

    @snippet.command(aliases = ["e"])
    async def edit(self, ctx, title, *, description):
        snippet = await self.get_snippet(ctx, title)
        if snippet.lock == 1:
            await ctx.send("This snippet is closed. Ask a moderator to unlock if you want to edit it. ")
            return
        else:
            if snippet.author_id == ctx.author.id:
                await self.bot.db.update("snippets", "description", description, "title", title)
                await ctx.send(f"Snippet {title} updated succesfully.")
            else:
                 await ctx.send("This snippet is not yours. Ask the author if you want to edit it.")

    @snippet.command(aliases = ["d"])
    async def delete(self, ctx, title):
        snippet = await self.get_snippet(ctx, title)
        if snippet.lock == 1:
            await ctx.send("This snippet is locked. Ask the author or a moderator to unlock it. ")
        elif snippet.author_id == ctx.author.id:
            await self.bot.db.delete("snippets", "title", title)
            await ctx.send(f"Snippet {title} deleted succesfully. ")
        elif ctx.author.guild_permissions.manage_messages:
            await self.bot.db.delete("snippets", "title", title)
            await ctx.send(f"Snippet {title} deleted succesfully. ")
        else:
            await ctx.send(f"You're not the author of {title} and don't have permission to do this. ")
    

    @snippet.command(aliases = ["lo"])
    async def lock(self, ctx, title: str):
        snippet = await self.get_snippet(ctx, title)
        if snippet.author_id != ctx.author.id and not ctx.author.guild_permissions.manage_messages:
            await ctx.send(f"You're not the author of {title} and don't have permission to do this. ")
        elif snippet.lock == 1:
            await ctx.send("This snippet is already locked. ")
        else:
            await self.bot.db.update("snippets", "locked", 1, "title", title)
            await ctx.send(f"Snippet {title} has been locked. ")


    @snippet.command(aliases = ["ul"])
    async def unlock(self, ctx, title: str):
        snippet = await self.get_snippet(ctx, title)
        if snippet.author_id != ctx.author.id and not ctx.author.guild_permissions.manage_messages:
            await ctx.send(f"You're not the author of {title} and don't have permission to do this. ")
            return
        elif snippet.lock == 0:
            await ctx.send("This snippet is already unlocked. ")
            return
        else:
            await self.bot.db.update("snippets", "locked", 0, "title", title)
            await ctx.send(f"Snippet {title} has been unlocked. ")    
    
    @snippet.command(name = "list", aliases = ["l"])
    async def snippet_list(self, ctx):
        group_result = await self.bot.db.get_all("snippets")
        message = ""
        if group_result == []:
            await ctx.send(f"{ctx.author.name} is a bitch. This will only be empty in tests. ")
            return
        for result in group_result:
            if result[3] == 1: # Lock check.
                message += f"— _*{result[0]}*_ :lock:\n" #Print the name of the snippets + lock emoji. 
            else:
                message += f"— _*{result[0]}*_ \n" # Print without lock emoji.
        await ctx.send(message)
        

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
        group_result = await self.bot.db.get_all_where("snippets", "author_id", user.id)
        message = ""
        if group_result == []:
            message = "This user hasn't made any snippets. "
        for result in group_result:
            if result[3]  == 1: # Lock check.
                message += f"— _*{result[0]}*_ :lock:\n" # Print the name of the snippets + lock emoji.
            else:
                message += f"— _*{result[0]}*_ \n" # Print without lock emoji.
        await ctx.send(message)       

async def setup(bot):
    await bot.add_cog(Snippets(bot))
