import discord
from os import environ

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
        elif message.content == 'pong':
            await message.channel.send('NO, YOU have to say ping and ONLY I get to say pong !')
        elif message.content == 'f':
            await message.channel.send('f')
        elif message.content == 'F':
            await message.channel.send('F')
    
    async def on_member_join(member):
        await member.add_roles(932799395865444382)

client = MyClient()
client.run(environ['CYBER_GHOST_TOKEN'])