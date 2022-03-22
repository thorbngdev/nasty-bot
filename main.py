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


@bot.event
async def on_message(ctx):
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


# comando de testes
@bot.command()
async def nasty(ctx, arg):
    await ctx.channel.send(f'{arg} NASTY')


@bot.event
async def on_member_update(before, after):
    print(f'{before.nick} alterado para {after.nick}')


@bot.event
async def on_voice_state_update(member, before, after):
    if before.self_deaf == False and after.self_deaf == True:
        await send_message_on_shitposting(f'{member.nick} se mutar vai levar um KIKAO NOS PEITO')
        await asyncio.sleep(60)
        if member.voice.self_deaf:
            await member.move_to(get_afk_channel())


async def send_message_on_shitposting(message):
    await bot.guilds[0].get_channel(165698427819130881).send(message)


def get_afk_channel():
    return bot.guilds[0].get_channel(165742812380397568)


bot.run(get_bot_token())