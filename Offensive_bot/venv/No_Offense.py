import discord
from discord.ext import commands
import random
import asyncio
import re
import os
import asyncpg
import json
from itertools import cycle
from lxml import html
from lxml import etree
import requests
import msgpack
from msgpack import pack
from msgpack import unpack

userName = "PappysTip"
pw = "YouM4yt4k3MyLIFE_Butt!"

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



TOKEN = open("cogs/lists/TOKEN", "r").read()
PG_PW = open("cogs/lists/PG_PW", "r").read()
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, description="A bot")
#remove default help command
bot.remove_command('help')


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database="NoOffense", user="postgres", password=PG_PW)


#initialize global lists for use in commands
fact = []
meanadj = []
meannoun = []
userMessage = []
uwu = ["uwu", "uwU", "uWu", "uWU", "Uwu", "UwU", "UWu", "UWU", "owo", "owO", "oWo", "oWO", "Owo", "OwO", "OWo", "OWO"]


#loads a file line by line into a list
async def loadFile(filename):
    return [line.rstrip('\n') for line in open(f'cogs/lists/{filename}', "r", encoding='utf-8')]


#simple function to load lists (TODO: improve it so it initializes all global lists without editing if possible)
async def generateLists():
    global meanadj
    global meannoun
    global userMessage
    meanadj = await loadFile('MeanAdjectives')
    meannoun = await loadFile('MeanNouns')
    userMessage = await loadFile('UserMessage')


@bot.event
async def on_ready():
    print(f'Logged in successfully: {bot.user.name}')
    print('----------------------------------------------')
    with open('cogs/lists/Reactions', 'w') as f:
        for emoji in bot.emojis:
            f.write(f"{emoji.name} : {emoji.id}\n")
    await generateLists()


@bot.command()
async def submit(ctx, *, submission: commands.clean_content):
    if len(submission) < 1:
        await ctx.send("You must actually submit something you dingus.")
        return
    if len(userMessage) > 1000:
        await ctx.send("Our depository for messages is full :(")
        return
    f = open('cogs/lists/UserMessage', 'a', encoding='utf-8')
    f.write(submission + "\n")
    f.close()
    userMessage.append(submission)

@bot.command()
async def testhtml(ctx):
    page = requests.get('https://www.realmeye.com/top-guilds-on-server/USMidWest2')
    tree = etree.parse(page.content)
    # This will create a list of buyers:
    print(tree.xpath('//td/a[text()]'))


@bot.command()
async def surprise(ctx):

    if (len(userMessage) < 1):
        await ctx.send("No messages to send")
        return
    messageToSend = random.choice(userMessage)
    await ctx.send(f'{messageToSend}')
    userMessage.remove(messageToSend)
    f = open('cogs/lists/UserMessage', 'w')
    for s in userMessage:
        f.write(s + "\n")


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colorr=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info: {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"request by: {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild Name:", value=member.display_name)
    embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Guild At:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Roles ({len(roles)}):", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role:", value=member.top_role.mention)
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)

@bot.command()
async def roast(ctx, target : discord.Member = None):
    target = ctx.author if not target else target
    await ctx.send(f"{target.mention} is a {random.choice(meanadj)}, {random.choice(meanadj)} {random.choice(meannoun)}")

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, cog):
    try:
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'{cog} was reloaded')
    except Exception as e:
            print(f"{cog} could not be reloaded:")
            raise(e)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def gay_ray(ctx, count : int):
    count = 1 if not count else count
    gay_dict = {}
    for x in range(int(count)):
        target = random.choice(ctx.guild.members)
        if not target in gay_dict:
            gay_dict.setdefault(target, 1)
        else:
            gay_dict[target] += 1
    for target in gay_dict:
        gay_count = gay_dict.get(target)
        if gay_count == 1:
            await ctx.send(f"{target.mention} is gay")
        elif gay_count == 2:
            await ctx.send(f"{target.mention} is big gay")
        elif gay_count == 3:
            await ctx.send(f"{target.mention} is super gay")
        elif gay_count == 4:
            await ctx.send(f"{target.mention} is mega gay")
        else:
            await ctx.send(f"{target.mention} is hyper gay")
        asyncio.sleep(1)

@bot.command()
@commands.has_permissions(administrator=True)
async def msgpacktest(ctx):
    data = {'a list': [1, 42, 3.141, 1337, 'help'],
            'a string': 'bla',
            'another dict': {'foo': 'bar',
                             'key': 'value',
                             'the answer': 42}}

    # Write msgpack file
    with open('cogs/lists/data.msgpack', 'w') as f:
        msgpack.dumps(data, f)

    # Read msgpack file
    with open('cogs/lists/data.msgpack', 'r') as f:
        data_loaded = msgpack.loads(f)

    await ctx.send(f'data == {data_loaded}')


for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded:")
            raise(e)


bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)
