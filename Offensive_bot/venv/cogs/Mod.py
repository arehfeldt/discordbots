import discord
from discord.ext import commands
import random
import asyncio


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No Reason"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked by {ctx.author.mention}.\n`{reason}`")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No Reason"):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was banned by {ctx.author.mention}.\n`{reason}`")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} messages deleted")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a member to kick")
        if isinstance(error, commands.BadArgument):
            await ctx.send("You entered an invalid member to kick")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions to do this")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a member to kick")
        if isinstance(error, commands.BadArgument):
            await ctx.send("You entered an invalid member to kick")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions to do this")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Must specify a number")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Your argument needs to be a number!")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions to do this")


def setup(bot):
    bot.add_cog(Mod(bot))