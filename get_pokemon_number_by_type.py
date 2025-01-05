import csv
import os
import json

class Pokemon:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

pokemon_datafile = os.path.join('data','pokemon.csv')
output_stats_datafile = os.path.join('pokemon_number_by_types.txt')

def load_data(datafile):
    with open(datafile,'r',encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        pokemons_data = [Pokemon(row) for row in csv_reader]
    return pokemons_data

pokemons_data = load_data(pokemon_datafile)

count_by_types = dict(
normal = 0,
fire = 0,
water = 0,
electric = 0,
grass = 0,
ice = 0,
fighting = 0,
poison = 0,
ground = 0,
flying = 0,
psychic = 0,
bug = 0,
rock = 0,
ghost = 0,
dragon = 0,
dark = 0,
steel = 0,
fairy = 0,
)

for pokemon in pokemons_data:
    for current_pokemon_type in pokemon.type1, pokemon.type2:
        if not current_pokemon_type == "":
            count_by_types[current_pokemon_type] += 1

sorted_types = dict(sorted(count_by_types.items(), key=lambda item: item[1],reverse=True))

with open(output_stats_datafile, 'w') as file:
    json.dump(sorted_types, file, indent=4)

os.system(f'start {output_stats_datafile}')