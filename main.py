import asyncio

from discord.ext import commands
from utils.credentials import get_bot_token
import discord

# documentation -> https://discordpy.readthedocs.io/en
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix='D.', intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} bora fecha porra!")
    bot.get_guild(165698427819130881).fetch_members()

    # while True:
    #     print('Heroku health-check!') # testar sem isso apos web to worker
    #     await asyncio.sleep(240)


@bot.event
async def on_message(ctx):
    try:
        if ctx.author == bot.user:
            return

        if ctx.content == 'pepen':
            await ctx.channel.send('só um barrilzao na tela')

        if ctx.content == 'murilo':
            await ctx.channel.send('Vc quis dizer.. MINGUBILI?')

        if ctx.content == 'galassi':
            await ctx.channel.send('https://imgur.com/LumBZES')

        if ctx.content == 'arthur':
            await ctx.channel.send('https://imgur.com/7HHV3A9')

        if ctx.content == 'artcrazy':
            await ctx.channel.send('https://imgur.com/kX39RAR')

        if ctx.content == 'rato lenhador' \
                or ctx.content == 'joints':
            await ctx.channel.send('https://imgur.com/Dz8JUY5')

        if ctx.content == 'eliguedes' \
                or ctx.content == 'eliezer':
            await ctx.channel.send('https://imgur.com/VzsuVei')

        if ctx.content == 'bora uma lowzinha':
            await ctx.channel.send('https://imgur.com/2nJD4yT')

        await bot.process_commands(ctx)
    except Exception as e:
        print(e.args)


# comando de testes
@bot.command()
async def nasty(ctx, arg):
    try:
        await ctx.channel.send(f'{arg} NASTY')
    except Exception as e:
        print(e.args)


@bot.event
async def on_member_update(before, after):
    try:
        print(f'{before.nick} alterado para {after.nick}')
    except Exception as e:
        print(e.args)


@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if after.self_deaf and not before.self_deaf:
            await send_message_on_shitposting(f'{member.nick} se mutar vai levar um KIKAO NOS PEITO')
            await asyncio.sleep(120)
            if member.voice.self_deaf:
                await member.move_to(get_afk_channel())
    except Exception as e:
        print(e.args)


async def send_message_on_shitposting(message):
    try:
        await bot.guilds[0].get_channel(165698427819130881).send(message)
    except Exception as e:
        print(e.args)


def get_afk_channel():
    return bot.guilds[0].get_channel(165742812380397568)


bot.run(get_bot_token())
