import discord
from discord.ext import commands
import random
import asyncio
import json


def get_prefix(bot, msg):
    if not msg.guild:
        return commands.when_mentioned_or("!")(bot, msg)

    with open("cogs/lists/Prefix", 'r') as f:
        prefixes = json.load(f)

    if str(msg.guild.id) not in prefixes:
        return commands.when_mentioned_or("!")(bot, msg)
    else:
        prefix = prefixes[str(msg.guild.id)]
        return commands.when_mentioned_or(prefix)(bot, msg)



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="help")
    async def help_(self, ctx):
        cmds = {
            f"{(get_prefix(self.bot, ctx.message))[2]}" : "prefix to interact with the bot and its commands",
            "submit [message]" : "submits your message to the bot",
            "surprise" : "gives a random user-provided message",
            "gay_ray [count]" : "gay rays [count] random people\nvarying levels of gayness depending on how many rays you swallowed",
            "userinfo [@member (opt.)]": "gives useful information about a discord member",
            "roast [target]": "roasts the target into oblivion",
            "lvlinfo [@member (opt.)]": "gives some information about a current members level",
            "realmeye [player]": "Launch an interactive interface with a players realmeye.",
            "set_prefix [prefix]" : "changes the prefix the bot uses for commands\nRequires administrator permissions",
            "clear [count]": "clear's [count] messages \n requires message managing permissions \n x defaults to 10",
            "kick [member] [reason]": "kick a member from the discord \n requires kicking permissions",
            "ban [member] [reason]": "ban a member from the discord \n requires banning permissions",
            "reload [cog]": "reloads a cog in the discord bot \n requires administrator permissions",
            "add_pr [presense]": "Only accessible to the bot owner (A-Aron) | add's a presense that the bot can cycle through",
            "del_pr" : "removes the current presense and cycles to the next",
            "chat queues" : "pikachu | fact | any form of uwu or owo | howdy | this is so sad",

        }
        embed = discord.Embed(color = ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name="Help", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
        for cmd in cmds:
            embed.add_field(name=cmd, value=cmds[cmd], inline=False)

        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Help(bot))