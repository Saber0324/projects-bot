import discord
import datetime
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = "No reason provided."):
        await user.kick(reason=reason)
        await ctx.send(f"{user.name} has been kicked. \nReason: {reason}")

    @commands.command()
    @commands.has_permissions(moderate_members = True)
    async def timeout(self, ctx, user: discord.Member, duration: int, *, reason: str = "No reason provided."):
        await user.timeout(datetime.timedelta(minutes=duration), reason=reason)
        await ctx.send(f"{user.name} has been timed out for {duration} minutes. \nReason: {reason}")

    @commands.command()
    @commands.has_permissions(moderate_members = True)
    async def untimeout(self, ctx, user: discord.Member):
        await user.timeout(None)
        await ctx.send(f"{user.name} has been unmuted.")

# Hog told me to not include it yet. Dont uncomment.
    # @commands.command()
    # @commands.has_permissions(ban_members = True)
    # async def ban(self, ctx, user: discord.Member, duration: int, *, reason: str = "No reason provided."):
    #     await user.ban(reason=reason)
    #     await ctx.send(f"{user.name} has been banned.")

    # @commands.command()
    # @commands.has_permissions(ban_members = True)
    # async def unban(self, ctx, user_id: int):
    #     user = await bot.fetch_user(user_id)
    #     await ctx.guild.unban(user)
    #     await ctx.send(f"{user.name} has been unbanned.")

# Needs proper implementation.
    # @commands.command()
    # @commands.has_permissions(ban_members = True)
    # async def tempban(self, ctx, user: discord.Member, duration: int, *, reason: str = "No reason provided.")
    #     await user.ban(reason=reason)
    #     await ctx.send(f"{user.name} has been banned for {duration} days. Reason: {reason}")

    @commands.group()
    @commands.has_permissions(manage_roles = True)
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Correct usage: \n`!role add @member role` \n`!role remove @member role`")

    @role.command()
    async def add(self, ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(f"The role {role.name} has been added to {user.name}.")

    @role.command()
    async def remove(self, ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        await ctx.send(f"The role {role.name} has been removed from {user.name}.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))