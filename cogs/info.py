import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong {round(self.bot.latency * 1000, 2)} ms!")
    
    @commands.command()
    async def userinfo(self, ctx: commands.Context, user: discord.Member):
        embed = discord.Embed(title="User Information", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="User Name", value=f"{user.name}", inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Roles", value=", ".join([r.mention for r in user.roles][1:][::-1]), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def serverinfo(self, ctx):
        server = ctx.guild
        embed = discord.Embed(title="Server Information", color=discord.Color.blue())
        embed.set_thumbnail(url=server.icon.url if server.icon else None)
        embed.add_field(name="Server Name", value=f":flag_do: {server.name}", inline=True)
        embed.add_field(name="Server ID", value=f"**{server.id}**", inline=True)
        embed.add_field(name="Owner", value=f":crown: {server.owner}", inline=True)
        embed.add_field(name="Member Count", value=server.member_count, inline=True)
        embed.add_field(name="Creation Date", value=server.created_at.strftime("%Y/%m/%d"), inline=False)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Info(bot))