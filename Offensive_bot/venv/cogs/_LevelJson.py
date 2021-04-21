import discord
from discord.ext import commands
import random
import asyncio
import re
import json

BOT_PREFIX = ("|")

class LevelJson(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.save_users())

        with open(r"C:\Users\16reh\PycharmProjects\Offensive_bot\venv\cogs\lists\users", "r") as f:
            self.users = json.load(f)


    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"C:\Users\16reh\PycharmProjects\Offensive_bot\venv\cogs\lists\users", "w") as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(10)

    def levelup(self, authorId):
        curXp = self.users[authorId]['xp']
        curLvl = self.users[authorId]['lvl']

        if curXp >=  round(10 + 2 * (curLvl ** (8/5))):
            self.users[authorId]['lvl'] += 1
            return True
        return False


    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        if author == self.bot.user:
            return
        authorId = str(message.author.id)

        if not authorId in self.users:
            self.users[authorId] = {}
            self.users[authorId]['lvl'] = 1
            self.users[authorId]['xp'] = 0

        self.users[authorId]['xp'] += 1

        if self.levelup(authorId):
            await channel.send(f"{author.mention} has leveled up to {self.users[authorId]['lvl']}\n"
                               f"Level {self.users[authorId]['lvl'] + 1} at {round(10 + 2 * (self.users[authorId]['lvl'] + 1) ** (8/5))} experience")
            self.users[authorId]['xp'] = 0;


    @commands.command()
    async def lvlinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        memberId = str(member.id)
        if not memberId in self.users:
            await ctx.send(f"{member.display_name} does not have a level")
        else:
            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f"Level Information - : {member}")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name="Current Level: ", value=self.users[memberId]['lvl'])
            embed.add_field(name="Current Experience: ", value=self.users[memberId]['xp'])
            embed.add_field(name="Messages to next level: ", value=round(10 + 2 * (self.users[memberId]['lvl'] + 1) ** (8/5) - self.users[memberId]['xp']))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LevelJson(bot))