import discord
from discord.ext import commands
import random
import asyncio
import json
import re


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, *, prefix):
        with open("cogs/lists/Prefix", 'r', encoding='utf-8') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        await ctx.send(f"New prefix for commands  has been set to '{prefix}'")
        with open("cogs/lists/Prefix", "w", encoding="utf-8") as f:
            json.dump(prefixes, f, indent=4)

    @set_prefix.error
    async def set_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a prefix")
        if isinstance(error, commands.BadArgument):
            await ctx.send("You entered an invalid argument")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions to do this")


def setup(bot):
    bot.add_cog(Admin(bot))