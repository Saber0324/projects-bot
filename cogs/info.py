import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(content=f"Pong {round(number=self.bot.latency * 1000, ndigits=2)} ms!")
    
    @commands.group()
    async def info(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Correct usage: \n`!info server` \n`!info user @user` \n`!info role (count/list/@role)`")

    @info.command()
    async def user(self, ctx: commands.Context, user: discord.Member) -> None:
        embed = discord.Embed(title="User Information", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="User Name", value=f"{user.name}", inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Roles", value=", ".join([r.mention for r in user.roles][1:][::-1]), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)
        
    @info.command()
    async def server(self, ctx: commands.Context) -> None:
        server = ctx.guild
        embed = discord.Embed(title="Server Information", color=discord.Color.blue())
        embed.set_thumbnail(url=server.icon.url if server.icon else None)
        embed.add_field(name="Server Name", value=f":flag_do: {server.name}", inline=True)
        embed.add_field(name="Server ID", value=f"**{server.id}**", inline=True)
        embed.add_field(name="Owner", value=f":crown: {server.owner}", inline=True)
        embed.add_field(name="Member Count", value=server.member_count, inline=True)
        embed.add_field(name="Creation Date", value=server.created_at.strftime("%Y/%m/%d"), inline=False)
        await ctx.send(embed=embed)

    @info.group(invoke_without_command=True)
    async def role(self, ctx: commands.Context, target: discord.Role = None) -> None:
        if ctx.invoked_subcommand is None:
            if target:
                embed = discord.Embed(title="Role Info", color=target.color)
                embed.add_field(name="Role Name", value=target.mention, inline=True)
                embed.add_field(name="Role ID", value=target.id, inline=False)
                embed.add_field(name="Member Count", value=len(target.members), inline=False)
                embed.add_field(name="Role Color", value=str(target.color), inline=False)
                await ctx.send(embed=embed)
            else:    
                await ctx.send(content="Correct usage: \n`!info role @role` \n`!info role list` \n`!info role count (group)`")

    @role.command(name="list")
    async def role_list(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title="Role List", color=discord.Color.blue())
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.add_field(name="Roles", value="\n".join([r.mention for r in ctx.guild.roles][1:][::-1]), inline=False)
        await ctx.send(embed=embed)

    @role.command()
    async def count(self, ctx: commands.Context, *, group: str = None) -> None:
        pass
    
async def setup(bot) -> None:
    await bot.add_cog(Info(bot))