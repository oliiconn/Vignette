import discord
from discord.ext import commands
import data.constants as vigne

class Moderation:

    def __init__(self, Vigne):
        self.Vigne = Vigne
        self.logs = Vigne.get_channel(446042011452309514)

# Bans the specified user.
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, banned:discord.Member=None):
        'Bans a user.\nThe person who issues the command must have the permissions to ban.\ni.e: v!ban @olicon#1488'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        if banned is None:
            await ctx.send(f"Tell me who to ban, {ctx.author.mention}!")
        else:
            try:
                await ctx.guild.ban(banned)
                self.logs.send(f"{banned.name}#{banned.discriminator} ({banned.id}) was banned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id} in {ctx.guild}!")
                await ctx.send(f"{banned.mention} [{banned.name}#{banned.discriminator}] ({banned.id}) was banned by {ctx.author.mention} [{ctx.author.name}#{ctx.author.discriminator}] ({ctx.author.id})!")
            except:
                await ctx.message.add_reaction(':PillowNo:444127065990496276')
                self.logs.send(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) just tried to kick {banned.name}#{banned.discriminator} ({banned.id} in {ctx.guild}!")
                await ctx.send(f"I can't ban that person! Sorry, {ctx.author.mention}.")


# Kicks the specified user.
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, *, kicked:discord.Member=None, kickreason:str=""):
        'Kicks a user.\nThe person who issues the command must have the permissions to kick.\ni.e: v!kick @olicon#1488'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        if kicked is None:
            await ctx.send(f"Tell me who to kick, {ctx.author.mention}!")
        else:
            try:
                await ctx.guild.kick(kicked, reason=kickreason)
                self.logs.send(f"{kicked.name}#{kicked.discriminator} ({kicked.id}) was kicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id} in {ctx.guild}!")
                await ctx.send(f"{kicked.mention} [{kicked.name}#{kicked.discriminator}] ({kicked.id}) was kicked by {ctx.author.mention} [{ctx.author.name}#{ctx.author.discriminator}] ({ctx.author.id})!")
            except:
                await ctx.message.add_reaction(':PillowNo:444127065990496276')
                await ctx.send(f"I can't kick that person! Sorry, {ctx.author.mention}.")
                self.logs.send(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) just tried to kick {kicked.name}#{kicked.discriminator} ({kicked.id} in {ctx.guild}!")


def setup(Vigne):
    Vigne.add_cog(Moderation(Vigne))
