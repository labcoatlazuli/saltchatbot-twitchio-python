

import os
from twitchio.ext import commands, routines
from twitchio import Message, Channel
from tinydb import TinyDB, Query
from tinydb.operations import increment, set

db = TinyDB('db.json')


TARGET_CHANNEL = 'shio_shisho'


class Bot(commands.Bot):
    current_channel = None

    current_stream_bruhs = 0

    last_message : Message = None

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='c1pll673k34lmlqzt6eodlfcuf1zg1', client_secret='g8h000jq1wbjn6iblcp6knj81n6ast', prefix='!', initial_channels=[TARGET_CHANNEL])
        
    async def event_channel_joined(self, channel: Channel):
        self.current_channel = channel
        print(f"Joined {self.current_channel.name}")
        await self.current_channel.send("Starting SaltBot v0.1.0")
        return await super().event_channel_joined(channel)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    

    async def event_message(self, message):
        if message.echo: # ignore bot-sent messages tagged with echo = True
            return

        self.last_message = message
        
        if message.content[0] != '!' and 'bruh' in "".join(message.content.lower().split()): #Check if string 'bruh' is in a message
            self.increment_bruhcount(message)
            await self.bruhcount_send()
            

        print(message.content) # Print contents of message to console

        await self.handle_commands(message)

    

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

    def init_if_bruh_count_no_exist(self):
        if db.search(Query().type == 'bruh_count') == []:
            print("inserting")
            db.insert( {'type': 'bruh_count', 'count': 0 } )

    def increment_bruhcount(self, message: Message):

        self.init_if_bruh_count_no_exist()

        db.update(increment('count'), Query().type == 'bruh_count')

        self.current_stream_bruhs += 1

    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.member)
    @commands.command()
    async def bruhcount(self, ctx: commands.Context):

        self.init_if_bruh_count_no_exist()
        
        await self.bruhcount_send()

    async def bruhcount_send(self):

        current_bruhs = self.current_stream_bruhs

        historical_bruhs = db.search(Query().type == 'bruh_count')[0].get('count')

        await self.current_channel.send(f"Bruhs this stream: {current_bruhs} | Historical bruh count: {historical_bruhs}")

    @commands.command()
    async def resethistoricalbruhs(self, ctx: commands.Context):
        if ctx.author.is_mod:
            db.update(set('count', 0), Query().type == 'bruh_count')
            await self.bruhcount_send()
        else:
            self.current_channel.send('Sorry, the historical bruh count can only be reset by a moderator.')


    @commands.command()
    async def resetcurrentbruhs(self, ctx: commands.Context):
        if ctx.author.is_mod:
            self.current_stream_bruhs = 0
            await self.bruhcount_send()
        else:
            self.current_channel.send('Sorry, the current stream bruh count can only be reset by a moderator.')

    @commands.command()
    async def bruhlore(self, ctx: commands.Context):

        await ctx.send(f"Once upon a bruh, and the ")
    

    # @routines.routine(minutes=15)
    # async def notification(self, ctx: commands.Context):
    #     if self.last_message.echo:
    #         ctx.send("[INFO] Before requesting, please use !sl for the song list. Live learns --> use channel points")

        





bot = Bot()
bot.run()