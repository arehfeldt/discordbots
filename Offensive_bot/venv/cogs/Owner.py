import discord
from discord.ext import commands
import random
import asyncio
import json
from itertools import cycle
import math
import re
from discord.utils import get

OWNER_ID = "174345940574928896"

statuses = list
status = str

async def is_bot_owner(ctx):
    return str(ctx.author.id) == OWNER_ID

async def loadFile(filename):
    return [line.rstrip('\n') for line in open(f'cogs/lists/{filename}', "r", encoding='utf-8')]

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.chng_pr())

    async def chng_pr(self):
        await self.bot.wait_until_ready()
        global statuses
        global status
        statuses = await loadFile("Status")
        statuses = cycle(statuses)
        while not self.bot.is_closed():
            status = next(statuses)
            if not status:
                await self.bot.change_presence(activity=discord.Game("with :fire:"))
            else:
                await self.bot.change_presence(activity=discord.Game(status))
            await asyncio.sleep(10)


    @commands.command()
    @commands.check(is_bot_owner)
    async def add_pr(self, ctx, *, status):
        with open('cogs/lists/Status', 'a', encoding='utf-8') as f:
            f.write(status + "\n")
        global statuses
        statuses = await loadFile("Status")
        statuses = cycle(statuses)

    @commands.command()
    @commands.check(is_bot_owner)
    async def add_champ(self, ctx, type, name, url):
        with open('cogs/lists/Champions', 'r', encoding='utf-8') as f:
            champions = json.load(f)
        with open('cogs/lists/Championsbackup', 'w', encoding='utf-8') as f:
            json.dump(champions, f, indent=4)
        champions[type].update({name: url})
        with open('cogs/lists/Champions', 'w', encoding='utf-8') as f:
            json.dump(champions, f, indent=4)

        statuses = await loadFile("Status")
        statuses = cycle(statuses)

    @commands.command()
    @commands.check(is_bot_owner)
    async def print_emojis(self, ctx):
        emojis = [self.bot.get_emoji(emoji.id) for emoji in self.bot.emojis]
        emLen = len(emojis)
        line1 = f"{emojis[0 :math.trunc(emLen/5)]}"
        line2 = f"{emojis[math.trunc(emLen/5) : math.trunc(2*emLen/5)]}"
        line3 = f"{emojis[math.trunc(2*emLen/5) : math.trunc(3*emLen/5)]}"
        line4 = f"{emojis[math.trunc(3*emLen/5) : math.trunc(4*emLen/5)]}"
        line5 = f"{emojis[math.trunc(4*emLen/5): emLen]}"
        await ctx.send("Printing Emojis!")
        await asyncio.sleep(1)
        await ctx.send(re.sub('[[\]\']', '', line1))
        print(re.sub('[[\]\']', '', line1))
        await asyncio.sleep(2)
        await ctx.send(re.sub('[[\]\']', '', line2))
        print(re.sub('[[\]\']', '', line2))
        await asyncio.sleep(2)
        await ctx.send(re.sub('[[\]\']', '', line3))
        print(re.sub('[[\]\']', '', line3))
        await asyncio.sleep(2)
        await ctx.send(re.sub('[[\]\']', '', line4))
        print(re.sub('[[\]\']', '', line4))
        await asyncio.sleep(3)
        await ctx.send(re.sub('[[\]\']', '', line5))
        print(re.sub('[[\]\']', '', line5))
        await ctx.send("Done!")




def setup(bot):
    bot.add_cog(Owner(bot))