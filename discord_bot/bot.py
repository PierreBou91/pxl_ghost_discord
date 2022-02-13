import discord
from discord.ext import commands
from os import environ
import db_discord_helper as db
import random
import aws_connect_helper as s3
import texts
import re

# Boilerplate code

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix='/',
    description="Discord bot on Heroku",
    intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# on_message

@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author.id == 931674481628434503:
        return

    if str(message.content).casefold() == 'ping':
        await message.channel.send('pong')
    elif str(message.content).casefold() == 'pong':
        await message.channel.send('NO, YOU have to say ping and ONLY I get to say pong !')
    elif str(message.content).casefold() == 'f':
        await message.channel.send('F')

    # giveaway channel id: 931945712290258994
    # testbot channel id: 931679915248594944

    if message.channel.id == 931945712290258994:
        if db.check_if_ongoing_giveaway():
            if not bool(re.match(r"^0x[a-fA-F0-9]{40}$", message.content)):
                await message.reply(texts.channel_reserved())
                await message.reply(texts.wrong_wallet_address())
        else:
            await message.channel.send(texts.no_ongoing_giveway())

    if bool(re.match(r"^0x[a-fA-F0-9]{40}$", message.content)):
        wallet_is_in_db, wallet_owner = db.wallet_already_in_db(
            message.content)
        if not wallet_is_in_db:
            db.add_wallet(db.member_adapter_from_discord(
                message.author), message.content)
        if db.check_if_ongoing_giveaway():
            # check if wallet matches the owner
            matches_author, wallet_owner = db.wallet_matches_onwer(
                db.member_adapter_from_discord(message.author), message.content)
            if not matches_author:
                await message.reply(texts.wallet_does_not_match(wallet_owner))
                return
            # check if user is already in the giveaway
            if db.check_if_member_in_giveaway(db.member_adapter_from_discord(message.author)):
                await message.reply(texts.member_already_in_giveaway())
            # add user to giveaway
            else:
                db.add_member_to_giveaway(
                    db.member_adapter_from_db(message.author))
                await message.reply(texts.successful_giveaway_register())
        else:
            await message.channel.send(texts.no_ongoing_giveway())

    # Necessary command for the command to work
    await bot.process_commands(message)

# General commands

@bot.command()
async def ghost(ctx, number: int):
    r = random.randint(1, 10000)
    try:
        if (number == 0):
            file = discord.File(s3.get_ghost(r), filename='ghost.png')
            await ctx.reply(file=file, content=f'''You called a random ghost, I'm the number {r}''')
        elif (number in (9903, 9904, 9905)):
            file = discord.File(s3.get_ghost(number), filename='ghost.png')
            await ctx.reply(file=file, content=f'''Hello, I'm the ghost number {number}''')
        elif (number > 9900 and number < 10001):
            file = file = discord.File(
                s3.get_ghost('mystery'), filename='ghost.png')
            await ctx.reply(file=file, content=f'''Hello, I'm the mystery ghost...''')
        else:
            file = discord.File(s3.get_ghost(number), filename='ghost.png')
            await ctx.reply(file=file, content=f'''Hello, I'm the ghost number {number}''')
    except Exception:
        await ctx.reply('You have to give a number between 1 and 10000')
        return


@bot.command()
async def rules(ctx):
    await ctx.send(texts.rules())

# Admin command

@bot.command()
@commands.has_any_role("Admin")
async def update_db(ctx):
    # Load members from server
    server_members_dict = {}
    for mem in ctx.guild.members:
        server_members_dict[str(mem.id)] = db.member_adapter_from_discord(mem)

    # Load members from db
    db_members_dict = db.get_all_members()

    # Update the "is_here" value
    has_left = []
    ids = []

    for id, mem in db_members_dict.items():
        if (id not in server_members_dict):
            has_left.append(mem)
        else:
            ids.append(str(id))

    db.update_is_here(has_left, False)

    # Update the memmbers that have changed
    have_changed = []

    for id in ids:
        if server_members_dict[id].nick != db_members_dict[id].nick:
            have_changed.append(server_members_dict[id])
        elif server_members_dict[id].display_name != db_members_dict[id].display_name:
            have_changed.append(server_members_dict[id])
        elif server_members_dict[id].top_role != db_members_dict[id].top_role:
            have_changed.append(server_members_dict[id])

    db.update_db(have_changed)

    await ctx.reply("Database updated ;D")


@bot.command()
@commands.has_any_role("Admin")
async def giveaway(ctx, is_owner=None):
    is_owner = True if (is_owner == "owner") else False
    is_only_giveaway = True if db.check_only_giveaway(is_owner) else False
    if is_only_giveaway:
        db.launch_giveaway(ctx, is_owner)
        await ctx.reply(texts.giveaway(is_owner))
    else:
        await ctx.reply(texts.already_giveaway(is_owner))


@bot.command()
@commands.has_any_role("Admin")
async def delete(ctx, giveaway_id):
    db.delete_giveaway(giveaway_id)

# On member join

@bot.event
async def on_member_join(member):
    await member.add_roles(932799395865444382)
    if not db.member_is_in_db(member):
        db.add_user(db.member_adapter_from_discord(member))
    else:
        memberlist = ()
        memberlist.append(db.member_adapter_from_discord(member))
        db.update_is_here(memberlist, True)

bot.run(environ['CYBER_GHOST_TOKEN'])
