import discord
from discord.ext import commands
import random
import asyncio
import json
import requests
import re
from discord.utils import get

TIMEOUT = 60

async def genOpen(bot, ctx, opponent, reactions):
    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"{ctx.author.display_name} has challenged {opponent} to a duel!\n\n\n"
    f"{ctx.author.display_name} Choose your BattleMon!")
    embed.set_thumbnail(url='https://freepngimg.com/download/boxing_gloves/5-2-boxing-gloves-transparent.png')
    for react in reactions:
        emoji = reactions
        embed.add_field(name=react, value=react.name)
    embed.set_footer(text=f"Duel request by: {ctx.author}", icon_url=ctx.author.avatar_url)
    return embed

async def getchamp(reaction, champions):
    if reaction == 'Random':
        reaction = random.choice(list(champions.keys()))
        print(reaction)
    champion = random.choice(list(champions[reaction].keys()))
    print(reaction)
    return [champion, champions[reaction][champion]]

async def addreacts(bot, message, reactions):
    for react in reactions:
        await message.add_reaction(react)

async def genresult(winner, loser, winnerchamp, loserchamp, winnerurl, loserurl, ctx):
    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    select = random.randint(1,10)
    if select == 1:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 2:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 3:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 4:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 5:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 6:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 7:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 8:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    if select == 9:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    else:
        embed.set_author(name=f"{winner.display_name}'s {winnerchamp} put {loser.display_name}'s {loserchamp} to shame", icon_url=winner.avatar_url)
    embed.set_image(url=winnerurl)
    embed.set_thumbnail(url=loserurl)
    embed.set_footer(text=f"Better luck next time {loser}", icon_url=loser.avatar_url)
    return embed

class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global champions




    @commands.command()
    async def duel(self, ctx, opponent : discord.Member = None):
        with open('cogs/lists/Champions', 'r', encoding='utf-8') as f:
            champions = json.load(f)

        for champ in champions:
            print(champions[champ].keys())
        opponent = ctx.author if not opponent else opponent
        if ctx.author.bot or opponent.bot:
            message = await ctx.send("Bot cannot be a challenger")
            await asyncio.sleep(5)
            await message.delete()
            return
        await ctx.message.delete()
        reactions = [
            get(self.bot.emojis, name="Politician"),
            get(self.bot.emojis, name="Animal"),
            get(self.bot.emojis, name="SchoolSupply"),
            get(self.bot.emojis, name="AnimeCharacter"),
            get(self.bot.emojis, name="Movie"),
            get(self.bot.emojis, name="Realm"),
            get(self.bot.emojis, name="Food"),
            get(self.bot.emojis, name="Hobby"),
            get(self.bot.emojis, name="GameCharacter"),
            get(self.bot.emojis, name="Misc"),
            get(self.bot.emojis, name="Random"),
            get(self.bot.emojis, name="Close")
        ]
        openEmbed = await genOpen(self.bot, ctx, opponent.display_name, reactions)
        message = await ctx.send(embed=openEmbed)
        await addreacts(self.bot, message, reactions)

        while True:
            try:
                react1, challenger  = await self.bot.wait_for('reaction_add', check=lambda r, c: not c.bot
                                                              and r.message.id == message.id and c.id == ctx.author.id and r.emoji in reactions,
                                                              timeout=TIMEOUT)
                if react1.emoji.name == 'Close':
                    closed_embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                    closed_embed.set_author(name=f"Duel aborted, cancelled by {ctx.author.display_name}")
                    closed_embed.set_image(
                        url=f'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/htc/37/cross-mark_274c.png')
                    closed_embed.set_thumbnail(
                        url="http://pngimg.com/uploads/exclamation_mark/exclamation_mark_PNG35.png")
                    await message.edit(embed=closed_embed)
                    await message.clear_reactions()
                    await asyncio.sleep(10)
                    await message.delete()
                    break

                else:
                    openEmbed.set_author(name= f"{ctx.author.display_name} has chosen {react1.emoji.name}!\n\n\n{opponent.display_name} Choose your BattleMon!")
                    await message.clear_reactions()
                    await message.edit(embed=openEmbed)
                    await addreacts(self.bot, message, reactions)
                    champ1 = []
                    champ1 = await getchamp(react1.emoji.name, champions)

                react2, challengee = await self.bot.wait_for('reaction_add', check=lambda r, c: not c.bot and r.message.id == message.id
                                                            and c.id == opponent.id and r.emoji in reactions,
                                                            timeout=TIMEOUT)


                if react2.emoji.name == 'Close':
                    closed_embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                    closed_embed.set_author(name=f"Duel aborted, cancelled by {opponent.display_name}")
                    closed_embed.set_image(
                        url=f'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/htc/37/cross-mark_274c.png')
                    closed_embed.set_thumbnail(
                        url="http://pngimg.com/uploads/exclamation_mark/exclamation_mark_PNG35.png")
                    await message.edit(embed=closed_embed)
                    await message.clear_reactions()
                    await asyncio.sleep(10)
                    await message.delete()
                    return
                else:
                    openEmbed.set_author(name=f"{opponent.display_name} has chosen {react2.emoji.name}!\n\n\n"
                                         f"Battle Commence!")
                champ2 = []
                champ2 = await getchamp(react2.emoji.name, champions)

                winner = random.choice([champ1, champ2])
                if winner == champ1:
                    embed = await genresult(ctx.author, opponent, champ1[0], champ2[0], champ1[1], champ2[1], ctx)
                else:
                    embed = await genresult(opponent, ctx.author, champ2[0], champ1[0], champ2[1], champ1[1], ctx)
                await message.edit(embed=embed)
                await message.clear_reactions()
                await asyncio.sleep(5)
                await asyncio.sleep(25)
                await message.delete()
                break
            except Exception as e:
                closed_embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                closed_embed.set_author(name=f"Duel aborted, BattleMon not chosen on time")
                closed_embed.set_image(
                    url=f'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/htc/37/cross-mark_274c.png')
                closed_embed.set_thumbnail(url="http://pngimg.com/uploads/exclamation_mark/exclamation_mark_PNG35.png")
                await message.edit(embed=closed_embed)
                await message.clear_reactions()
                print(e)
                await asyncio.sleep(10)
                await message.delete()
                raise(e)
                break





def setup(bot):
    bot.add_cog(Duel(bot))
