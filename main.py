import asyncio
import io
from datetime import date
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

conn = psycopg2.connect(
    host="ec2-54-158-247-210.compute-1.amazonaws.com",
    # port="5432",
    database="de5rt2tk2avjul",
    user="ckorztxaspjroe",
    password="3af5f3741222f9aefff79c23ed555a7eb70772984171394052417ffacec55cf5")


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

        if ctx.content == 'ultimo avistamento':
            await ctx.channel.send('https://cdn.discordapp.com/attachments/'
                                   '165698427819130881/958925528138657832/unknown.png')

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
                                   'find -> encontra um pokemon\n'
                                   'catch (soon) -> tenta capturar o pokemon\n'
                                   'pokedex (soon) -> lista seus pokemons```')
        if args == 'find':
            pokedex_threshold = 987
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={pokedex_threshold}')
            pokemon_list = list(map(lambda p: p['name'], response.json()['results']))
            random_pokemon = pokemon_list[randint(0, (pokedex_threshold - 1))]
            pokemon_json = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_pokemon}').json()
            pokemon = Pokemon(json=pokemon_json)
            sprite = f"http://play.pokemonshowdown.com/sprites/xyani/{pokemon.name}.gif"
            async with aiohttp.ClientSession() as session:
                async with session.get(sprite) as resp:
                    data = io.BytesIO(await resp.read())
                    await ctx.channel.send(f'Le wild {pokemon.pretty_name} appears\n'
                                           f'Type: {pokemon.type_str}\n'
                                           f'``HP: {pokemon.hp} / '
                                           f'Attack: {pokemon.attack} / '
                                           f'Defense: {pokemon.defense} / '
                                           f'S. Attack: {pokemon.special_attack} / '
                                           f'S. Defense: {pokemon.special_defense} / '
                                           f'Speed: {pokemon.speed}``',
                                           file=discord.File(data, f'{pokemon.name}.gif'))

        if args == 'claim':
            response = insert_pokeball(ctx)
            await ctx.channel.send(response)

        if args == 'bag' or args == 'galassi':
            # response = insert_pokeball(ctx)
            # await ctx.channel.send(response)
            pass

        if args == 'catch':
            # insert_pokemon(ctx, pokemon)
            # print(f'{ctx.author.name} capturou um {pokemon.name}')
            pass
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
        if list(map(lambda r: r.id, member.roles)).count(356668830417944577) != 0:
            return

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


def insert_pokeball(ctx):
    today = date.today()
    message = ''
    normal = randint(5, 9)
    great = randint(3, 5)
    ultra = randint(0, 3)
    master = 1 if randint(0, 10) == 2 else 0
    cursor = conn.cursor()
    cursor.execute('select * from pokeball where discord_id = %s', (ctx.author.id,))
    obtained = cursor.fetchone()
    if not obtained:
        cursor.execute('insert into pokeball'
                       '(check_date, discord_id, discord_name, normal, great, ultra, master)'
                       ' values (%s, %s, %s, %s, %s, %s, %s)',
                       (today, ctx.author.id, ctx.author.name, normal, great, ultra, master))
        conn.commit()
        message =   '```' \
                    '- Loot -\n' \
                    f'Obteve {normal} Pokeballs\n' \
                    f'Obteve {great} Great Balls\n' \
                    f'Obteve {ultra} Ultra Balls\n' \
                    f'Obteve {master} Master Balls\n\n' \
                    '- Bag -\n' \
                    f'Pokeball: {normal}\n' \
                    f'Great Ball: {great}\n' \
                    f'Ultra Ball: {ultra}\n' \
                    f'Master Ball: {master}' \
                    '```'
    elif today == obtained[1]:
        message = 'Ja pegou hoje carai'
    else:
        cursor.execute('update pokeball set normal = %s, great = %s, ultra = %s, master = %s,'
                       ' check_date = %s'
                       ' where discord_id = %s', (normal + int(obtained[4]),
                                                 great + int(obtained[5]),
                                                 ultra + int(obtained[6]),
                                                 master + int(obtained[7]),
                                                 today,
                                                 ctx.author.id,))
        conn.commit()
        message =   '```' \
                    '- Loot -\n' \
                    f'Obteve {normal} Pokeballs\n' \
                    f'Obteve {great} Great Balls\n' \
                    f'Obteve {ultra} Ultra Balls\n' \
                    f'Obteve {master} Master Balls\n\n' \
                    '- Bag -\n' \
                    f'Pokeball: {normal + int(obtained[4])}\n' \
                    f'Great Ball: {great + int(obtained[5])}\n' \
                    f'Ultra Ball: {ultra + int(obtained[6])}\n' \
                    f'Master Ball: {master + int(obtained[7])}' \
                    '```'

    cursor.close()
    return message


bot.run(get_bot_token())
