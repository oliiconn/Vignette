import discord
from discord.ext import commands
import data.constants as vigne
import praw
import random
import requests


class NSFW:


    def __init__(self, Vigne):
        self.Vigne = Vigne

    
    @commands.command()
    async def hentai(self, ctx, hentaisubreddit=None):
        'Posts a hentai image from a selection of NSFW subreddits.'
        pornoembed = discord.Embed(color=discord.Color.purple())
        if ctx.channel.is_nsfw():
            if hentaisubreddit is None:
                sub = vigne.reddit.subreddit(random.choice(vigne.hentaisubreddit18))
                pornoembed.set_author(name=f'/r/{sub}', icon_url='http://benance.xyz/BreadBotCDN/Reddit-icon.png')
                pornoimage = sub.random() 
                pornoembed.set_footer(text=pornoimage.url, icon_url=ctx.author.avatar_url)
                if pornoimage.url.endswith(('.jpg', '.jpeg', '.gif', '.png')):
                    pornoembed.set_image(url=pornoimage.url)
                elif pornoimage.url.startswith(('https://imgur.com/a/', 'http://imgur.com/a/')):
                    imgurhandler = pornoimage.url[-7:]
                    response = requests.get(f'https://api.imgur.com/3/album/{imgurhandler}/images', headers={'Authorization': 'Client-ID 0be828cc1ef298e'}).json['data'][0]['link']
                    pornoembed.set_image(url=response)
                elif pornoimage.url.startswith(('https://imgur.com', 'http://imgur.com')):
                    imgurhandler = pornoimage.url[-7:]
                    pornoembed.set_image(url=f'https://i.imgur.com/{imgurhandler}.jpg')
                await ctx.send(embed=pornoembed)
            else:
                if hentaisubreddit in vigne.hentaisubreddit18:
                    sub = vigne.reddit.subreddit(hentaisubreddit)
                    pornoembed.set_author(name=f'/r/{sub}', icon_url='http://benance.xyz/BreadBotCDN/Reddit-icon.png')
                    pornoimage = sub.random()
                    pornoembed.set_footer(text=pornoimage.url, icon_url=ctx.author.avatar_url)
                    if pornoimage.url.endswith(('.jpg', '.jpeg', '.gif', '.png')):
                        pornoembed.set_image(url=pornoimage.url)
                    elif pornoimage.url.startswith(('https://imgur.com/a/', 'http://imgur.com/a/')):
                        imgurhandler = pornoimage.url[-7:]
                        response = requests.get(f'https://api.imgur.com/3/album/{imgurhandler}/images', headers={'Authorization': 'Client-ID 0be828cc1ef298e'}).json['data'][0]['link']
                        pornoembed.set_image(url=response)
                    elif pornoimage.url.startswith(('https://imgur.com/', 'http://imgur.com/')):
                        imgurhandler = pornoimage.url[-7:]
                        pornoembed.set_image(url=f"https://i.imgur.com/{imgurhandler}.jpg")
                    await ctx.send(embed=pornoembed)
                    print(pornoimage.url)
                else:   
                    await ctx.send("You didn't enter a valid `subreddit!` The valid `subreddits` are:\n```" + ", ".join(vigne.hentaisubreddit18) + "```\nRemember that the command is **case-sensitive!**")
        else:
            await ctx.send("This channel is not marked as `NSFW!` :warning:")


    @commands.command()
    async def porn(self, ctx, pornsubreddit=None):
        'Posts a pornographic image from a selection of NSFW subreddits.'
        pornoembed = discord.Embed(color=discord.Color.purple())
        if ctx.channel.is_nsfw():
            if pornsubreddit is None:
                sub = vigne.reddit.subreddit(random.choice(vigne.pornsubreddit18))
                pornoembed.set_author(name=f'/r/{sub}', icon_url='http://benance.xyz/BreadBotCDN/Reddit-icon.png')
                pornoimage = sub.random() 
                pornoembed.set_footer(text=pornoimage.url, icon_url=ctx.author.avatar_url)
                if pornoimage.url.endswith(('.jpg', '.jpeg', '.gif', '.png')):
                    pornoembed.set_image(url=pornoimage.url)
                elif pornoimage.url.startswith(('https://imgur.com/a/', 'http://imgur.com/a/')):
                    imgurhandler = pornoimage.url[-7:]
                    response = requests.get(f'https://api.imgur.com/3/album/{imgurhandler}/images', headers={'Authorization': 'Client-ID 0be828cc1ef298e'}).json['data'][0]['link']
                    pornoembed.set_image(url=response)
                elif pornoimage.url.startswith(('https://imgur.com', 'http://imgur.com')):
                    imgurhandler = pornoimage.url[-7:]
                    pornoembed.set_image(url=f'https://i.imgur.com/{imgurhandler}.jpg')
                await ctx.send(embed=pornoembed)
            else:
                if pornsubreddit in vigne.pornsubreddit18:
                    sub = vigne.reddit.subreddit(pornsubreddit)
                    pornoembed.set_author(name=f'/r/{sub}', icon_url='http://benance.xyz/BreadBotCDN/Reddit-icon.png')
                    pornoimage = sub.random()
                    pornoembed.set_footer(text=pornoimage.url, icon_url=ctx.author.avatar_url)
                    if pornoimage.url.endswith(('.jpg', '.jpeg', '.gif', '.png')):
                        pornoembed.set_image(url=pornoimage.url)
                    elif pornoimage.url.startswith(('https://imgur.com/a/', 'http://imgur.com/a/')):
                        imgurhandler = pornoimage.url[-7:]
                        response = requests.get(f'https://api.imgur.com/3/album/{imgurhandler}/images', headers={'Authorization': 'Client-ID 0be828cc1ef298e'}).json['data'][0]['link']
                        pornoembed.set_image(url=response)
                    elif pornoimage.url.startswith(('https://imgur.com/', 'http://imgur.com/')):
                        imgurhandler = pornoimage.url[-7:]
                        pornoembed.set_image(url=f"https://i.imgur.com/{imgurhandler}.jpg")
                    await ctx.send(embed=pornoembed)
                    print(pornoimage.url)
                else:   
                    await ctx.send("You didn't enter a valid `subreddit!` The valid `subreddits` are:\n```" + ", ".join(vigne.pornsubreddit18) + "```\nRemember that the command is **case-sensitive!**")
        else:
            await ctx.send("This channel is not marked as `NSFW!` :warning:")


def setup(Vigne):
    Vigne.add_cog(NSFW(Vigne))