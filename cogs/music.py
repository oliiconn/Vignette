import asyncio
import functools
import logging
import os
import pathlib

import discord
import discord.ext.commands as commands
import youtube_dl


def setup(Vigne):
    Vigne.add_cog(Music(Vigne))


def duration_to_str(duration):
    # Extract minutes, hours and days
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    # Create a fancy string
    duration = []
    if days > 0: duration.append(f'{days} days')
    if hours > 0: duration.append(f'{hours} hours')
    if minutes > 0: duration.append(f'{minutes} minutes')
    if seconds > 0 or len(duration) == 0: duration.append(f'{seconds} seconds')

    return ', '.join(duration)

class MusicError(commands.UserInputError):
    pass


class Song(discord.PCMVolumeTransformer):
    def __init__(self, song_info):
        self.info = song_info.info
        self.requester = song_info.requester
        self.channel = song_info.channel
        self.filename = song_info.filename
        super().__init__(discord.FFmpegPCMAudio(self.filename, before_options='-nostdin', options='-vn'))


class SongInfo:
    ytdl_opts = {
        'default_search': 'auto',
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'source_address': '0.0.0.0', # Make all connections via IPv4
        'nocheckcertificate': True,
        'restrictfilenames': True,
        'logger': logging.getLogger(__name__),
        'logtostderr': False,
        'no_warnings': True,
        'quiet': True,
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'noplaylist': True
    }
    ytdl = youtube_dl.YoutubeDL(ytdl_opts)

    def __init__(self, info, requester, channel):
        self.info = info
        self.requester = requester
        self.channel = channel
        self.filename = info.get('_filename', self.ytdl.prepare_filename(self.info))
        self.downloaded = asyncio.Event()
        self.local_file = '_filename' in info

    @classmethod
    async def create(cls, query, requester, channel, loop=None):
        try:
            # Path.is_file() can throw a OSError on syntactically incorrect paths, like urls.
            if pathlib.Path(query).is_file():
                return cls.from_file(query, requester, channel)
        except OSError:
            pass

        return await cls.from_ytdl(query, requester, channel, loop=loop)

    @classmethod
    def from_file(cls, file, requester, channel):
        path = pathlib.Path(file)
        if not path.exists():
            raise MusicError(f'File {file} not found.')

        info = {
            '_filename': file,
            'title': path.stem,
            'creator': 'local file',
        }
        return cls(info, requester, channel)

    @classmethod
    async def from_ytdl(cls, request, requester, channel, loop=None):
        loop = loop or asyncio.get_event_loop()

        # Get sparse info about our query
        partial = functools.partial(cls.ytdl.extract_info, request, download=False, process=False)
        sparse_info = await loop.run_in_executor(None, partial)

        if sparse_info is None:
            raise MusicError(f'Could not retrieve info from input : {request}')

        # If we get a playlist, select its first valid entry
        if "entries" not in sparse_info:
            info_to_process = sparse_info
        else:
            info_to_process = None
            for entry in sparse_info['entries']:
                if entry is not None:
                    info_to_process = entry
                    break
            if info_to_process is None:
                raise MusicError(f'Could not retrieve info from input : {request}')

        # Process full video info
        url = info_to_process.get('url', info_to_process.get('webpage_url', info_to_process.get('id')))
        partial = functools.partial(cls.ytdl.extract_info, url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise MusicError(f'Could not retrieve info from input : {request}')

        # Select the first search result if any
        if "entries" not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise MusicError(f'Could not retrieve info from url : {info_to_process["url"]}')

        return cls(info, requester, channel)

    async def download(self, loop):
        if not pathlib.Path(self.filename).exists():
            partial = functools.partial(self.ytdl.extract_info, self.info['webpage_url'], download=True)
            self.info = await loop.run_in_executor(None, partial)
        self.downloaded.set()

    async def wait_until_downloaded(self):
        await self.downloaded.wait()

    def __str__(self):
        title = f"**{self.info['title']}**"
        creator = f"**{self.info.get('creator') or self.info['uploader']}**"
        duration = f" (**Duration:** {duration_to_str(self.info['duration'])})" if 'duration' in self.info else ''
        return f'{title} from {creator}{duration}'


class Playlist(asyncio.Queue):
    def __iter__(self):
        return self._queue.__iter__()

    def clear(self):
        for song in self._queue:
            try:
                os.remove(song.filename)
            except:
                pass
        self._queue.clear()

    def get_song(self):
        return self.get_nowait()

    def add_song(self, song):
        self.put_nowait(song)

    def __str__(self):
        info = '**__My queue!__**\n'
        info_len = len(info)
        for song in self:
            s = str(song)
            l = len(s) + 1 # Counting the extra \n
            if info_len + l > 1995:
                info += '[...]'
                break
            info += f'{s}\n'
            info_len += l
        return info


class GuildMusicState:
    def __init__(self, loop):
        self.playlist = Playlist(maxsize=50)
        self.voice_client = None
        self.loop = loop
        self.player_volume = 0.5
        self.skips = set()
        self.min_skips = 5

    @property
    def current_song(self):
        return self.voice_client.source

    @property
    def volume(self):
        return self.player_volume

    @volume.setter
    def volume(self, value):
        self.player_volume = value
        if self.voice_client:
            self.voice_client.source.volume = value

    async def stop(self):
        self.playlist.clear()
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    async def play_next_song(self, song=None, error=None):
        if error:
            await self.current_song.channel.send(f'An error has occurred while playing {self.current_song}: {error}')

        if song and not song.local_file and song.filename not in [s.filename for s in self.playlist]:
            os.remove(song.filename)

        if self.playlist.empty():
            await self.stop()
        else:
            next_song_info = self.playlist.get_song()
            await next_song_info.wait_until_downloaded()
            source = Song(next_song_info)
            source.volume = self.player_volume
            self.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(next_song_info, e), self.loop).result())
            await next_song_info.channel.send(f'**Singing:** {next_song_info}')


class Music:
    def __init__(self, Vigne):
        self.Vigne = Vigne
        self.music_states = {}

    def __unload(self):
        for state in self.music_states.values():
            self.Vigne.loop.create_task(state.stop())

    def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command cannot be used in a private message.')
        return True

    async def __before_invoke(self, ctx):
        ctx.music_state = self.get_music_state(ctx.guild.id)

    async def __error(self, ctx, error):
        if not isinstance(error, commands.UserInputError):
            raise error

        try:
            await ctx.send(error)
        except discord.Forbidden:
            pass # /shrug

    def get_music_state(self, guild_id):
        return self.music_states.setdefault(guild_id, GuildMusicState(self.Vigne.loop))



    @commands.command()
    async def queue(self, ctx):
        'Displays the queue for music.'
        await ctx.send(f'{ctx.music_state.playlist}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        'Makes Vigne join the voice channel specified.\nIf there is no channel specified, it will join the channel the user is in.'
        if channel is None and not ctx.author.voice:
            raise MusicError("You didn't tell me where to go! `Join a voice channel or specify one for me to join.`")

        destination = channel or ctx.author.voice.channel

        if ctx.voice_client:
            await ctx.voice_client.move_to(destination)
        else:
            ctx.music_state.voice_client = await destination.connect()

    @commands.command()
    async def play(self, ctx, *, request: str):
        'Plays a song or adds it to the queue.\nUses Youtube-DL to fetch songs.'
        await ctx.message.add_reaction('\N{HOURGLASS}')

        # Create the SongInfo
        song = await SongInfo.create(request, ctx.author, ctx.channel, loop=ctx.bot.loop)

        # Connect to the voice channel if needed
        if ctx.voice_client is None or not ctx.voice_client.is_connected():
            await ctx.invoke(self.join)

        # Add the info to the playlist
        try:
            ctx.music_state.playlist.add_song(song)
        except asyncio.QueueFull:
            raise MusicError('The queue is full, sorry! Try again later.')
            await ctx.message.add_reaction(':PillowNo:444127065990496276')

        if not ctx.music_state.is_playing():
            # Download the song and play it
            await song.download(ctx.bot.loop)
            await ctx.music_state.play_next_song()
        else:
            # Schedule the song's download
            ctx.bot.loop.create_task(song.download(ctx.bot.loop))
            await ctx.send(f'Okay! {song} is now queued for **#{ctx.music_state.playlist.qsize()}**!')

        await ctx.message.remove_reaction('\N{HOURGLASS}', ctx.me)
        await ctx.message.add_reaction(':PillowYes:444889434270334978')

    #@commands.command()
    #async def np(self, ctx):
     #   'Displays the song that is currently playing.'
     #   if ctx.music_state.is_playing():
     #       await ctx.send(f'**Singing:** {song}. | `Volume:`{song.volume * 100}%. | `Channel:` {ctx.voice_client.channel.mention}')
     #   else:
     #       await ctx.send('Nothing is playing right now! Sorry.')

    @play.error
    async def play_error(self, ctx, error):
        await ctx.message.remove_reaction('\N{HOURGLASS}', ctx.me)
        await ctx.message.add_reaction(':PillowNo:444127065990496276')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def pause(self, ctx):
        """Pauses the player."""
        if ctx.voice_client:
            ctx.voice_client.pause()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def resume(self, ctx):
        """Resumes the player."""
        if ctx.voice_client:
            ctx.voice_client.resume()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def stop(self, ctx):
        """Stops the player, clears the playlist and leaves the voice channel."""
        await ctx.music_state.stop()

    @commands.command()
    async def volume(self, ctx, volume: int = None):
        """Sets the volume of the player, scales from 0 to 100."""
        if volume < 0 or volume > 100:
            raise MusicError('The volume level has to be between 0 and 100.')
        ctx.music_state.volume = volume / 100

    @commands.command()
    async def clear(self, ctx):
        'Clears the queue.'
        ctx.music_state.playlist.clear()

    @commands.command()
    async def skip(self, ctx):
        'Votes to skip the playing song.'
        if not ctx.music_state.is_playing():
            raise MusicError('How can you skip if nothing is playing? Silly!')

        if ctx.author.id in ctx.music_state.skips:
            raise MusicError(f"{ctx.author.mention}, you can't vote to skip twice!")

        # Count the vote
        ctx.music_state.skips.add(ctx.author.id)
        await ctx.message.add_reaction(':PillowYes:444889434270334978')

        # Check if the song has to be skipped
        if len(ctx.music_state.skips) > ctx.music_state.min_skips or ctx.author == ctx.music_state.current_song.requester:
            ctx.music_state.skips.clear()
            ctx.voice_client.stop()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def minskips(self, ctx, number: int):
        'Sets the minimum number of votes to skip a song.\nRequires the `Manage Guild` permission.'
        ctx.music_state.min_skips = number
