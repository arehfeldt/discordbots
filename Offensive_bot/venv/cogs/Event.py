import discord
from discord.ext import commands
import random
import asyncio
import re
import json
from discord.utils import get

async def loadFile(filename):
    return [line.rstrip('\n') for line in open(f'cogs/lists/{filename}', "r", encoding='utf-8')]

adj = list
noun = list
fact = list
howdy = list
whooosh = list

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



class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.load_lists())

    async def load_lists(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            global adj
            global noun
            global fact
            global howdy
            global whooosh
            adj = await loadFile(r"MeanAdjectives")
            noun = await loadFile(r"MeanNouns")
            fact = await loadFile(r"Facts")
            howdy = await loadFile(r"Howdy")
            whooosh = await loadFile(r"whooosh")
            await asyncio.sleep(50)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permissions to do that you {random.choice(adj)}, {random.choice(adj)} "
                           f"{random.choice(noun)}")
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"You {random.choice(adj)} {random.choice(noun)}! Thats not even a real command!")



        raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        guild =  "" if not message.guild else message.guild
        if author.bot:
            if re.search('messages deleted', content, re.IGNORECASE):
                await asyncio.sleep(5)
                await message.delete()
            return
        #print(f"{author}: {content}   \n-- FROM --\n {guild}: #{channel}\n")
        if content.startswith('help'):
            await channel.send(f"Use '{(get_prefix(self.bot, message))[2]}' to interact with me\n"
                               f"Or use'{(get_prefix(self.bot, message))[2]}'help to get a list of commands")
        if re.search('fact', content, re.IGNORECASE):
            await channel.send('did {} say *fact*?'.format(author))
            await channel.send(random.choice(fact))

        if content.startswith(str((get_prefix(self.bot, message))[2]) + "roast") or content.startswith((get_prefix(self.bot, message)[2]) + 'submit'):
            await asyncio.sleep(1)
            await message.delete()


        if re.match('this is so sad', content, re.IGNORECASE):
            await channel.send('https://cdn.discordapp.com/attachments/475330728490696715/568849231293448193/Video_4.mp4')


        if re.search('pikachu', content, re.IGNORECASE):
            load = {}
            with open("cogs/lists/Pikachu", 'r', encoding='utf-8') as f:
                pika = json.load(f)

            pikaRaw = pika[random.choice(list(pika.keys()))]
            await channel.send(f"```\n{pikaRaw}\n```")



        if re.search('uwu', content, re.IGNORECASE) or re.search('owo', content, re.IGNORECASE) \
                or re.search('owu', content, re.IGNORECASE) or re.search('uwo', content, re.IGNORECASE)\
                or re.search('xD', content, re.IGNORECASE) or re.search(':3', content, re.IGNORECASE):
            #await channel.send(f"***YAY!***\t**\\\\(^D^)/**\t***{author.mention} is super gay!***")
            await message.add_reaction(get(self.bot.emojis, name='Gay'))


        if re.search('howdy ', content, re.IGNORECASE):
            greet = [f"Yee Haw, {author}", "Put Em Up", "Dyin aint much of livin", "Get outta dodge"]
            embed = discord.Embed(color=author.color)
            embed.set_author(name="It's High Noon.")
            embed.set_image(url=random.choice(howdy))
            embed.set_footer(text=f"{random.choice(greet)}!")

            await channel.send(embed=embed)
        if re.search('hmm', content, re.IGNORECASE):
            embed = discord.Embed(color=author.color)
            embed.set_author(name="HMMMMMMMMMMMMMMMMMMM")
            embed.set_image(url="https://j.gifs.com/lx2j8l.gif")
            embed.set_footer(text="HMMMMMMMMMMMMMMMMMMM!")
            await channel.send(embed=embed)
        if re.search('whoosh', content, re.IGNORECASE) or re.search('whooosh', content, re.IGNORECASE) or re.search('whoooosh', content, re.IGNORECASE) or \
                re.search('whoooosh', content, re.IGNORECASE) or re.search('r/whoo', content, re.IGNORECASE):
            global whooosh
            await channel.send(f'{whooosh[0]}')
            await  message.delete()


def setup(bot):
    bot.add_cog(Event(bot))