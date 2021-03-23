import discord
from discord.ext import commands
import random
import re
import asyncpg




class MsgLevel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        if author == self.bot.user:
            return
        if not message.guild:
            return
        authorID = str(message.author.id)
        guildID = str(message.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM  users WHERE userid = $1 AND guildid = $2", authorID, guildID)

        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (userid, guildid, lvl, xp) VALUES ($1, $2, 1, 0)", authorID, guildID)

        user = await self.bot.pg_con.fetchrow("SELECT * FROM  users WHERE userid = $1 AND guildid = $2", authorID, guildID)
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE userid = $2 AND guildid =$3", user['xp'] + 1, authorID, guildID)



        if await self.levelup(user):
            await channel.send(f"{author.mention} has leveled up to {user['lvl'] + 1}\n"
                               f"Level {user['lvl'] + 2} at {round(10 + 2 * (user['lvl'] + 2) ** (8/5))} messages")
            await self.bot.pg_con.execute("UPDATE users SET xp = 0 WHERE userid = $1 AND guildid = $2", authorID, guildID)


    async def levelup(self, user):
        curXp = user['xp']
        curLvl = user['lvl']

        if curXp >= round(10 + 2 * (curLvl ** (8 / 5))):
            await self.bot.pg_con.execute("UPDATE users SET lvl = $1 WHERE userid = $2 AND guildid =$3", curLvl + 1,
                                    user['userid'], user['guildid'])
            return True
        return False


    @commands.command()
    async def lvlinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        memberID = str(member.id)
        guildID = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM  users WHERE userid = $1 AND guildid = $2", memberID,
                                              guildID)

        if not user:
            await ctx.send(f"{member.display_name} does not have a level")
        else:
            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f"Level Information - : {member}")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name="Current Level: ", value=user[0]['lvl'])
            embed.add_field(name="Current Experience: ", value=user[0]['xp'])
            embed.add_field(name="Messages to next level: ", value=round(10 + 2 * (user[0]['lvl'] + 1) ** (8/5) - user[0]['xp']))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MsgLevel(bot))