import asyncio
import io
from random import randint

import aiohttp
import discord
import psycopg2
import requests
from discord.ext import commands

from model.pokemon import Pokemon
from utils.credentials import get_bot_token

# documentation -> https://discordpy.readthedocs.io/en/stable/api.html
# bot def
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix='&', intents=intents, help_command=None)

# db defs
conn = psycopg2.connect(
    host="ec2-54-157-79-121.compute-1.amazonaws.com",
    # port="5432",
    database="d23etf932b1cba",
    user="mdmmavxkjavxkp",
    password="3438cbc07422437ad8343729d07663c9b299fbf26d0209edb726e1854834a167")



@bot.event
async def on_ready():
    print(f"{bot.user} bora fecha porra!")
    bot.get_guild(165698427819130881).fetch_members()


@bot.event
async def on_message(ctx):
    try:
        if ctx.author == bot.user:
            return

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


@bot.command()
async def help(ctx):
    try:
        await ctx.channel.send('HELP?? kkj')
    except Exception as e:
        print(e.args)


@bot.command()
async def pokefai(ctx, args):
    try:
        if args == 'help':
            await ctx.channel.send('```'
                                   'catch -> captura um pokemon\n'
                                   'pokedex (soon) -> lista seus pokemons```')
        if args == 'catch':
            pokedex_threshold = 987
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={pokedex_threshold}')
            pokemon_list = list(map(lambda p: p['name'], response.json()['results']))
            random_pokemon = pokemon_list[randint(0, (pokedex_threshold - 1))]
            pokemon_json = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_pokemon}').json()
            pokemon = Pokemon(json=pokemon_json)
            insert_pokemon(ctx, pokemon)
            print(f'{ctx.author.name} capturou um {pokemon.name}')
            async with aiohttp.ClientSession() as session:
                async with session.get(pokemon.front_sprite) as resp:
                    data = io.BytesIO(await resp.read())
                    await ctx.channel.send(f'Le wild {pokemon.pretty_name} appears\n'
                                           f'Type: {pokemon.type_str}\n'
                                           f'``HP: {pokemon.hp} / '
                                           f'Attack: {pokemon.attack} / '
                                           f'Defense: {pokemon.defense} / '
                                           f'S. Attack: {pokemon.special_attack} / '
                                           f'S. Defense: {pokemon.special_defense} / '
                                           f'Speed: {pokemon.speed}``',
                                           file=discord.File(data, f'{pokemon.name}.png'))

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
            await asyncio.sleep(600)
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


def insert_pokemon(ctx, pokemon):
    shiny = 1 if randint(0, 1000) == 500 else 0
    cursor = conn.cursor()
    cursor.execute('select * from pokedex where discord_id = %s and pokemon_id = %s and shiny = %s',
                   (ctx.author.id, pokemon.id, shiny,))
    obtained = cursor.fetchone()

    if obtained:
        cursor.close()
        return

    cursor.execute('insert into pokedex'
                   '(discord_id, discord_name, pokemon_id, pokemon_name,'
                   ' pokemon_type, front_sprite, back_sprite, shiny)'
                   ' values (%s, %s, %s, %s, %s, %s, %s, %s)',
                   (ctx.author.id, ctx.author.name, pokemon.id, pokemon.name, pokemon.type_str,
                    pokemon.shiny_front_sprite if shiny else pokemon.front_sprite,
                    pokemon.shiny_back_sprite if shiny else pokemon.back_sprite,
                    shiny))
    conn.commit()
    cursor.close()


bot.run(get_bot_token())
