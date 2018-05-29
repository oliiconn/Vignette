import discord
from discord.ext import commands
import data.constants as vigne
import os
import sys

class Special:
    def __init__(self, Vigne):
        self.Vigne = Vigne
        self.logs = Vigne.get_channel(446042011452309514)

# Restarts the bot. Not to normally be used.
    @commands.group(invoke_without_command=True, hidden=True)
    async def special(self, ctx, argument=None):
        'Permission check.'
        if ctx.author.id not in vigne.special:
            await ctx.message.add_reaction(':PillowNo:444127065990496276')

    @special.command()
    async def restart(self, ctx):
        'Restarts the bot.\nOnly accessible by people with full access to the bot.'
        if ctx.author.id not in vigne.special:
            await ctx.message.add_reaction(':PillowNo:444127065990496276')
        else:
            await ctx.message.add_reaction(':PillowYes:444889434270334978')
            await ctx.send("Alright! Restarting...")
            await self.logs.send(f"I have been restarted by {ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator}) [{ctx.author.id}].")
            print("Restarting!")
            await os.execl(sys.executable, sys.executable, *sys.argv)
    
    @special.command()
    async def leave(self, ctx):
        'Forces the bot to leave the server.\nOnly accessible by people with full access to the bot.'
        if ctx.author.id not in vigne.special:
            await ctx.message.add_reaction(':PillowNo:44412706599046276')
        else:
            await ctx.message.add_reaction(':PillowYes:444889434270334978')
            await ctx.send("Alright! Leaving...")
            await self.logs.send(f"I have been commanded to leave {ctx.guild.name} by {ctx.author.mention}.\nInformation: `Channel ID:` {ctx.channel.id} | `Guild ID:` {ctx.guild.id} | `Username:` {ctx.author.name}#{ctx.author.discriminator} | `User ID:` {ctx.author.id}")
            await ctx.guild.leave()
    
  #  @special.command()
  #  async def guildban(self, ctx, guildID:int):
   #     'Bans the bot from the guild. Will ban from the context guild if no ID is returned.'
  #      try:
   #         if guildID is None:
   #             guildID = ctx.guild.id
  ##          else:
   #             guildID = ctx.message
   #     except:
    #        await ctx.send("You must input a message ID.")
#
   #     bannedguild = Vigne.get_guild(guildID)

        
    
        

# Speaks through the bot.
    @special.command()
    async def say(self, ctx, *, arg):
        'Says text.\nTakes the argument from "v!say" and repeats it without the command prefix.\ni.e: v!say lol'
        if ctx.author.id not in vigne.special:
            await ctx.message.add_reaction(':PillowNo:444127065990496276')
        else:
            await ctx.send(arg)

def setup(Vigne):
    Vigne.add_cog(Special(Vigne))