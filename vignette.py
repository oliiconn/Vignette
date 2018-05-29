import discord
import asyncio
from discord.ext import commands
from discord.utils import find
import data.constants as vigne
import json
import logging

Vigne = commands.Bot(description="Vignette, ready to help! 😈⭐", command_prefix="v!")
logging.basicConfig(level=logging.INFO)


async def rotator():
    await Vigne.wait_until_ready()
    while True:
        userscount = 0
        channelscount = 0
        for guild in Vigne.guilds:
            channelscount += len(guild.channels)
        for user in Vigne.users:
            if user.bot is not True:
                userscount +=  1
        activities = [discord.Activity(type=3, name = f"{channelscount} channels! 😇 | v!help"),
        discord.Activity(type=2, name=f"{userscount} users! 😜 | v!help"),
        discord.Game(f"with {len(Vigne.guilds)} servers! 😏 | v!help")]
        for activity in activities:
            await Vigne.change_presence(activity=activity)
            await asyncio.sleep(10 * 60)  

@Vigne.event
async def on_ready():
      
    for cog in vigne.cogs:

        try:
            Vigne.load_extension(f'cogs.{cog}')
            print(f"Yay! The {cog} cog successfully loaded! :)")
            
        except Exception as e:
            print(f"Oh no! The {cog} cog failed to load! :(")
            print(e)

    userscount = 0    
    for user in Vigne.users:  
        if user.bot is True:
            continue
        else:
            userscount = userscount + 1

    guildscount = 0
    for guild in Vigne.guilds:
        guildscount = guildscount + 1

    channelscount = 0
    for guild in Vigne.guilds:
        for channel in guild.channels:
            channelscount = channelscount + 1
    print("Vignette is online and ready for action!")
    print(f"Overseeing {guildscount} servers, containing {channelscount} channels and {userscount} users.")

@Vigne.event
async def on_guild_join(guild):
    logs = Vigne.get_channel(446042011452309514)

    if guild.id not in vigne.banned_guilds:
        try:
            logs.send(f"I joined {guild.name}! `Guild ID:` {guild.id}")
            general = find(lambda x: 'general' in x.name,  guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send("Hello, `{}`, I'm **Vignette!**\n    — I'm a multi-purpose bot that's in development *(but with stable functionality!)*.\n    — To see all of my commands, do **v!help**!".format(guild.name))
        except:
            pass
    else:
        await logs.send(f"I tried to join `{guild.name}`` [**{guild.id}**], but it was registered as a *Banned Guild!*")
        await asyncio.sleep(5)
        await guild.leave()

Vigne.loop.create_task(rotator())

# runs the bot using the token from constants.py        
Vigne.run(vigne.token)
