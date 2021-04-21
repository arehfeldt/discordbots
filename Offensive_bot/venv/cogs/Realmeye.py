import discord
from discord.ext import commands
import random
import asyncio
import json
import requests
import re
from discord.utils import get

realm_icons = {}
max_stats = {}

async def genchars(bot, ctx, info):
    charEmbs = {}
    for char in info["characters"]:
        charClass = char['class']
        classEmote = get(bot.emojis, name=charClass)
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.add_field(name=f"Class: ", value=f"{classEmote}")
        embed.add_field(name=f"Level: ", value=f"{char['level']}")
        embed.add_field(name=f"Fame: ", value=f"{char['fame']}")
        embed.add_field(name=f"Rank: ", value=f"#{char['place']} in the world")
        equip = "\n".join(gear for gear in char['equipment'])
        statsRaw = [f"HP: {char['stats']['hp']} / {max_stats['hp'][f'{charClass}']}\t\tMP: {char['stats']['mp']} / {max_stats['mp'][f'{charClass}']}",
                    f"ATT: {char['stats']['attack']} / {max_stats['attack'][f'{charClass}']}\t\tDEF: {char['stats']['defense']} / {max_stats['defense'][f'{charClass}']}",
                    f"SPD: {char['stats']['speed']} / {max_stats['speed'][f'{charClass}']}\t\tDEX: {char['stats']['dexterity']} / {max_stats['dexterity'][f'{charClass}']}",
                    f"VIT: {char['stats']['vitality']} / {max_stats['vitality'][f'{charClass}']}\t\tWIS: {char['stats']['wisdom']} / {max_stats['wisdom'][f'{charClass}']}"]
        stats = "\n".join(rawstats for rawstats in statsRaw)
        embed.add_field(name=f"Equipment: ", value=f"{equip}", inline=False)
        embed.add_field(name=f"Stats: {char['stats_maxed']}", value=f'{stats}', inline=False)
        charEmbs.setdefault(charClass, embed)
    return charEmbs

async def genclosed(bot, ctx, info):
    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_image(url=f'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/htc/37/cross-mark_274c.png')
    embed.set_thumbnail(url='https://www.realmeye.com/s/cx/img/eye-big.png')
    embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
    return embed

async def genhome(bot, ctx, info):
    name = info['name']
    if {info['skins']} == -1:
        skinCount = 'Hidden'
    else:
        skinCount = info['skins']
    if {info['characterCount']} == -1:
        charCount = 'Hidden'
    else:
        charCount = info['characterCount']
    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.add_field(name=f"Characters: ", value=f"{charCount}")
    embed.add_field(name=f"Alive Fame: ", value=f"{info['fame']}")
    embed.add_field(name=f"Skins: ", value=f"{skinCount}")
    embed.add_field(name=f"Rank: ", value=f"{info['rank']} :star:")
    embed.add_field(name=f"Account Fame: ", value=f"{info['account_fame']}")
    embed.add_field(name=f"Guild: ", value=f"{info['guild']}")
    embed.add_field(name=f"Guild Rank: ", value=f"{info['guild_rank']}")
    embed.add_field(name=f"Created: ", value=f"{info['created']}")
    embed.add_field(name=f"Last Seen: ", value=f"{info['last_seen']}")
    description = "\n".join([desc for desc in info['description']])
    description = "No Description" if not description else description
    embed.add_field(name=f"Description:", value=f'{description}', inline=False)
    embed.set_author(name=f"Realmeye info of: {name}")
    embed.set_image(url=f'https://www.realmeye.com/signature-of/{name}')
    embed.set_thumbnail(url='https://www.realmeye.com/s/cx/img/eye-big.png')
    embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
    return embed

async def addreacts(bot, message, info):
    reacts = []
    react = get(bot.emojis, name='Home')
    reacts.append(react)
    await message.add_reaction(react)
    for class_name in info['characters']:
        react = get(bot.emojis, name=class_name['class'])
        reacts.append(react)
        await message.add_reaction(react)
    react = get(bot.emojis, name='Close')
    await message.add_reaction(react)
    reacts.append(react)
    return reacts

async def genselect(bot, ctx, info):
    closed_embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    closed_embed.set_image(
        url=f'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/htc/37/cross-mark_274c.png')
    closed_embed.set_thumbnail(url='https://www.realmeye.com/s/cx/img/eye-big.png')
    closed_embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"Error: {info['error']}\nPerhaps you meant one of these?\n\n")
    embed.set_thumbnail(url='https://www.realmeye.com/s/cx/img/eye-big.png')
    embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
    select = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, 10)]
    close = get (bot.emojis, name='Close')
    select.append(close)
    numSug = len(info['suggestions'])
    for x in range(0, 9):
        if x == numSug:
            break
        embed.add_field(name=f"{x + 1}: {info['suggestions'][x]}", value="----------------", inline=False)

    message = await ctx.send(embed=embed)
    reacts = []
    for x in range(0, 9):
        if x == numSug:
            break
        await message.add_reaction(select[x])
        reacts.append(select[x])
    await message.add_reaction(close)
    reacts.append(close)
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add',
                                                check=lambda r, u:
                                                not u.bot
                                                and r.message.id == message.id
                                                and u.id == ctx.author.id
                                                and r.emoji in reacts, timeout=300)
            print(reaction)
            if reaction == get(bot.emojis, name="Warrior"):
                print(reaction)
            else:
                closed_embed.set_author(
                    name=f"Task ended.\nReason: closed by {ctx.author.display_name}")
                await message.edit(embed=closed_embed)
                await message.clear_reactions()
                await asyncio.sleep(10)
                await message.delete()
                break

        except Exception as e:
            closed_embed.set_author(name=f"Task ended\nReason: 5 minute inactivity")
            await message.edit(embed=closed_embed)
            await message.clear_reactions()
            await asyncio.sleep(3)
            await message.delete()
            raise(e)
            break

async def genplayer(bot, ctx, info):
    player_embeds = {}
    closed_embed = await genclosed(bot, ctx, info)
    player_embeds = await genchars(bot, ctx, info)
    home_embed = await genhome(bot, ctx, info)
    name = info['name']
    for embed in player_embeds:
        player_embeds[embed].set_author(name=f"Realmeye info of: {name}")
        player_embeds[embed].set_image(url=f'https://www.realmeye.com/signature-of/{name}')
        player_embeds[embed].set_thumbnail(url='https://www.realmeye.com/s/cx/img/eye-big.png')
        player_embeds[embed].set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)
    message = await ctx.send(embed=home_embed)
    reacts = await addreacts(bot, message, info)
    await ctx.message.delete()
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add',
                                                     check=lambda r, u:
                                                     not u.bot
                                                     and r.message.id == message.id
                                                     and u.id == ctx.author.id
                                                     and r.emoji in reacts, timeout=300)
            if reaction.emoji.name == 'Home':
                await message.edit(embed=home_embed)
                await message.remove_reaction(emoji=reaction.emoji, member=user)
            elif reaction.emoji.name == 'Close':
                closed_embed.set_author(name=f"Task for Player {info['name']}.\nReason: closed by {ctx.author.display_name}")
                await message.edit(embed=closed_embed)
                await message.clear_reactions()
                await asyncio.sleep(10)
                await message.delete()
                break
            else:
                name = reaction.emoji.name
                new_embed = player_embeds[name]
                await message.edit(embed=new_embed)
                await message.remove_reaction(emoji=reaction.emoji, member=user)
        except Exception:
            closed_embed.set_author(name=f"Task for Player {info['name']}\nReason: 5 minute inactivity")
            await message.edit(embed=closed_embed)
            await message.clear_reactions()
            await asyncio.sleep(10)
            await message.delete()
            break



class Realmeye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global realm_icons
        global max_stats
        with open("cogs/lists/ROTMGStats", 'r', encoding='utf-8') as f:
            max_stats = json.load(f)




    @commands.command()
    async def realmeye(self, ctx, name):
        info = requests.get(f"http://www.tiffit.net/RealmInfo/api/user?u={name.replace(' ', '%20')}")
        info = info.json()
        closed_embed = await genclosed(self.bot, ctx, info)
        if 'error' in info:
            player_name = await genselect(self.bot, ctx, info)
            info = requests.get(f"http://www.tiffit.net/RealmInfo/api/user?u={player_name.replace(' ', '%20')}")
            info = info.json()
        await genplayer(self.bot, ctx, info)







def setup(bot):
    bot.add_cog(Realmeye(bot))