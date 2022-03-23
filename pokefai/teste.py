# lugar usado para testar recursos para a construçao do pokefai
# Como vai ser?
from random import randint

import pokebase
import requests


response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')
pokemon_list = list(map(lambda p: p['name'], response.json()['results']))
pokemon_name = pokemon_list[randint(0, 150)]
pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
print(pokemon.json())
# name = 'pikachu'
# moves = pokebase.pokemon(name).moves
#
# for m in moves:
#     print(m.move.name)

# fai