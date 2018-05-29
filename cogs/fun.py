import discord
from discord.ext import commands
import requests
import time
import random
import re
import data.constants as vigne



class Fun:

    def __init__(self, Vigne):
        self.Vigne = Vigne

    @commands.command()
    async def dice(self, ctx):
        'Rolls the dice! Let the fates decide.' 
        m = await ctx.send("You rolled a...")
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()

        dice = random.randint(1, 6)
        if dice == 1:
            await m.edit(content="You rolled a **1!** <:Dice1:447666198352625664>")
        elif dice == 2:
            await m.edit(content="You rolled a **2!** <:Dice2:447666197752709141>")
        elif dice == 3:
            await m.edit(content="You rolled a **3!** <:Dice3:447666206493638671>")
        elif dice == 4:
            await m.edit(content="You rolled a **4!** <:Dice4:447666207018057738>")
        elif dice == 5:
            await m.edit(content="You rolled a **5!** <:Dice5:447666207064195072>")
        elif dice == 6:
            await m.edit(content="You rolled a **6!** <:Dice6:447666207026315264>")



    @commands.command()
    async def quote(self, ctx):
        'Posts a random quote.'
        response = requests.get('https://talaikis.com/api/quotes/random/')
        response_data = response.json()
        author = response_data['author']
        quote = response_data['quote']
        result = (f'*"{quote}"* —**{author}**')
        await ctx.send(result)

# Posts an image of a cat from random.cat
    @commands.command()
    async def cat(self, ctx):
        'Posts a random image of a cat.'
        try:
            await ctx.trigger_typing()
            await self.Vigne.wait_until_ready()
            catEmbed = discord.Embed(color=discord.Color.purple())
            try:
                response = requests.get("http://aws.random.cat/meow").json()
                catEmbed.set_author(name=f"Fetched by {ctx.author.name}#{ctx.author.discriminator}!", icon_url=ctx.author.avatar_url)
                catEmbed.set_image(url=(response["file"]))
                catEmbed.set_footer(icon_url=ctx.author.avatar_url, text=(response["file"]))
                await ctx.send(embed=catEmbed)
            except:
                catEmbed.set_author(name=f"Fetched by {ctx.author.name}#{ctx.author.discriminator}!", icon_url=ctx.author.avatar_url)
                catEmbed.set_image(url=(random.choice(vigne.cats)))
                catEmbed.set_footer(icon_url=ctx.author.avatar_url, text=(random.choice(vigne.cats)))
                await ctx.send(embed=catEmbed)
        except:
            await ctx.send("An error has occurred. If this persists, contact `olicon#1488`.")

    @commands.command()
    async def dog(self, ctx):
        'Posts a random image of a puppers.'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random").json()
            dogEmbed = discord.Embed(color=discord.Color.purple())
            dogEmbed.set_author(name=f"Fetched by {ctx.author.name}#{ctx.author.discriminator}!", icon_url=ctx.author.avatar_url)
            dogEmbed.set_image(url=(response["message"]))
            dogEmbed.set_footer(icon_url=ctx.author.avatar_url, text=(response["message"]))
            await ctx.send(embed=dogEmbed)
        except:
            await ctx.send("Error. Either the API has failed or an error has occurred. If this persists, contact `olicon#1488`.")

    @commands.command()
    async def laugh(self, ctx):
        'posts a fucking troll face'
        await ctx.send("http://i0.kym-cdn.com/entries/icons/original/000/000/091/TrollFace.jpg")

    @commands.command()
    async def v8ball(self, ctx):
        'Asks the Magic 8 Ball a question.'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()

        answers = ["It is certain.", "It is decidely so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "You can count on it.", "As I see it, yes.", "Most likely.", 
        "Outlook good.", "Yes.", "Signs point to yes.", "Absolutely.", "Reply is hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
        "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.", "Chances aren't good."]

        if ctx.message.content.endswith("?"):
            await ctx.send(":8ball: " + random.choice(answers))
        else:
            await ctx.send("You didn't give the Magic 8 Ball a question! `(Must end with ?)`")
    
    @commands.command()
    async def bruhcat(self, ctx):
        'bruh cat'
        bruhcatEmbed = discord.Embed(color=discord.Color.purple())
        bruhcatEmbed.set_image(url='http://vignette.ga/dazedandconfused/6uyve.gif')
        await ctx.send(embed=bruhcatEmbed)
# Edits the message to display different emotes.
    @commands.command()
    async def wrong(self, ctx):
        'WRONG'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        m = await ctx.send('<:Wrongald:443907785982214157>')
        time.sleep(1)
        await m.edit(content='<:WrongaldCharge:443907906295824396>')
        time.sleep(1)
        await m.edit(content='<:WrongblastCharge:443907919692431391>')
        time.sleep(1)
        await m.edit(content='<:WrongBlast:443907938852012041>')

def setup(Vigne):
    Vigne.add_cog(Fun(Vigne))
