import discord
from discord.ext import commands
from os import environ
import db_discord_helper as db

bot = commands.Bot(
    command_prefix='/',
    description="Test discord bot on Heroku",
    intents=discord.Intents.default())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user:
        return

    if message.content == 'eltesto':
        await message.channel.send('ONLY ONE DYNO')

@bot.command()
async def add_user(ctx, wallet):
    db.add_user(ctx, wallet)

@bot.command()
async def test(ctx):
    await ctx.send("Heroku works")

bot.run(environ['CYBER_GHOST_TOKEN'])