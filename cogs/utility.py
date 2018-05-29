import discord
from discord.ext import commands
import data.constants as vigne
from datetime import datetime
class Utility:
    def __init__(self, Vigne):
        self.Vigne = Vigne

# Displays the mentioned users avatar. If no user is selected, the command issuers avatar is displayed.
    @commands.command()
    async def avatar(self, ctx, *, getUserV:discord.Member=None):
        'Shows a users avatar.\nMention a user as an argument and it will display their avatar.\nIf nobody is mentioned and the command is issued on its own, the person who issued the command will have their avatar displayed.\n i.e: v!avatar @olicon#1488'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        if getUserV is None:
            getUserV = self.Vigne.get_user(ctx.author.id)  

        avatarEmbed = discord.Embed(color=discord.Color.purple())
        avatarEmbed.set_author(name=f"Fetched by {ctx.author.name}#{ctx.author.discriminator}!", icon_url=ctx.author.avatar_url)
        
        if getUserV.avatar_url.endswith('.gif'):    
            avatarEmbed.set_image(url=getUserV.avatar_url_as(size=1024))
        else:
            avatarEmbed.set_image(url=getUserV.avatar_url_as(format='png', size=1024))
        avatarEmbed.set_footer(text=f"{getUserV.name}#{getUserV.discriminator}'s avatar", icon_url=getUserV.avatar_url)
        await ctx.send(embed=avatarEmbed)

# Displays the mentioned users details. If no user is selected, the command issuers details are displayed.
    @commands.command()
    async def profile(self, ctx, profileMember:discord.Member=None):
        'Displays user details in an embed.\nDisplays name, discriminator, mention, ID, creation date and online status.'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        if profileMember is None:
            profileMember = ctx.author
               
        profileEmbed = discord.Embed(color=discord.Color.purple())
        profileEmbed.set_thumbnail(url=profileMember.avatar_url)
        profileEmbed.set_author(name=f"{profileMember.name}#{profileMember.discriminator}", icon_url=profileMember.avatar_url)
        profileEmbed.add_field(name='Name', value=profileMember.mention)
        profileEmbed.add_field(name='ID', value=f"{profileMember.id}")
        cdvariable1 = str(discord.utils.snowflake_time(profileMember.id))[-15:-7]
        creationdate = datetime.strptime(cdvariable1, "%H:%M:%S")
        gjdvariable1 = str(profileMember.joined_at)[-15:-7]
        guildjoindate = datetime.strptime(gjdvariable1, "%H:%M:%S")
        profileEmbed.add_field(name='Creation Date', value="`" + str(discord.utils.snowflake_time(profileMember.id))[-26:-16] + " " + creationdate.strftime("%I:%M:%S %p") + "`")
        profileEmbed.add_field(name='Guild Join Date', value="`" + str(profileMember.joined_at)[-26:-16]+ " " + guildjoindate.strftime("%I:%M:%S %p") + "`")
        if ctx.author.status is discord.Status.dnd:
            profileEmbed.add_field(name='Online Status', value="**Busy** :heart:")
        elif profileMember.status is discord.Status.idle:
            profileEmbed.add_field(name='Online Status', value="**Idle** :yellow_heart:")
        elif profileMember.status is discord.Status.online:
            profileEmbed.add_field(name='Online Status', value="**Online** :green_heart:")
        elif profileMember.status is discord.Status.offline:
            profileEmbed.add_field(name='Online Status', value="**Offline** :black_heart:")
        await ctx.send(embed=profileEmbed)
            
# Displays information about the server which the message was sent in.
    @commands.command()
    async def server(self, ctx):
        'Displays details about the servers in an embed.\nShows guild name, owner, owners ID, creation date and number of members.'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        emoji_tuple = ctx.guild.emojis
        real_emojis = map(str, emoji_tuple)
        serverEmojis = ' '.join(real_emojis)
        serverEmbed = discord.Embed(color=discord.Color.purple())
        serverEmbed.set_thumbnail(url=ctx.guild.icon_url)
        serverEmbed.add_field(name='Name', value=ctx.guild.name)
        serverEmbed.add_field(name='Owner', value=ctx.guild.owner.mention)
        serverEmbed.add_field(name='Region', value=ctx.guild.region)
        serverEmbed.add_field(name='Owner ID', value=ctx.guild.owner.id)
        gcavariable1 = str(ctx.guild.created_at)[-15:-7]
        guildcreatedat = datetime.strptime(gcavariable1, "%H:%M:%S")
        serverEmbed.add_field(name='Creation Date', value="`" + str(ctx.guild.created_at)[-26:-16] + " " + guildcreatedat.strftime("%I:%M:%S %p") + "`")
        serverEmbed.add_field(name='# of Members', value=ctx.guild.member_count)
        serverEmbed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url_as(size=1024))
        await ctx.send(embed=serverEmbed)
        await ctx.send(f"**__Guild Emojis:__**\n{serverEmojis}")


# Displays bot credits.
    @commands.command()
    async def credits(self, ctx):
        'Shows credits.'
        await ctx.trigger_typing()
        await self.Vigne.wait_until_ready()
        olicon = self.Vigne.get_user(398252254022598666)
        benance = self.Vigne.get_user(178318490355105792)
        SilverMight = self.Vigne.get_user(181047289857441796)
        creditsEmbed = discord.Embed(color=discord.Color.purple())
        creditsEmbed.set_thumbnail(url=olicon.avatar_url)
        creditsEmbed.set_author(name="Credits", icon_url=olicon.avatar_url)
        creditsEmbed.add_field(name='Bot Creator', value=f"{olicon.name}#{olicon.discriminator} (398252254022598666)", inline=False)
        creditsEmbed.add_field(name='Created Using', value="Python, with [__discord.py@rewrite__](https://github.com/Rapptz/discord.py), made by [__Rapptz__](https://github.com/Rapptz)",inline=False)
        creditsEmbed.add_field(name='Media Outlets', value="[__Twitter__](https://twitter.com/oIicon), [__Website__](https://vignette.ga), [__YouTube__](https://www.youtube.com/channel/UCj4QBOCq4Q68SU677wOCw6Q)",inline=False)
        creditsEmbed.add_field(name='Special Thanks To', value=f"{benance.name}#{benance.discriminator}, for inspiring me to make a bot. [__breadbot__](https://github.com/breadbot-dev/breadbot/)\n{SilverMight.name}#{SilverMight.discriminator}, for hosting the bot. [__Website__](https://silvermight.com)",inline=False)
        creditsEmbed.add_field(name='Server Link', value="[__Discord__](https://discord.gg/YDyf2Ph), join if you need help or just to talk.")
        creditsEmbed.add_field(name='Bot Invite', value="[__Invite__](https://discordapp.com/api/oauth2/authorize?client_id=441740372188725268&permissions=70371334&scope=bot)")
        await ctx.send(embed=creditsEmbed)

    @commands.command()
    async def invite(self, ctx):
        'DMs an invite link for the bot.'
        try:
            await ctx.message.add_reaction(':PillowYes:444889434270334978')
            await ctx.author.send("https://discordapp.com/api/oauth2/authorize?client_id=441740372188725268&permissions=70371334&scope=bot")
        except:
            try:
                await ctx.message.add_reaction(':PillowNo:444127065990496276')
            except:
                await ctx.trigger_typing()
                await ctx.send("I can't Direct Message you!")

        
def setup(Vigne):
    Vigne.add_cog(Utility(Vigne))