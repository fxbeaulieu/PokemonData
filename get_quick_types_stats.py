import csv
import os
import yaml

class Pokemon:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

pokemon_datafile = os.path.join('data','pokemon.csv')
types_chart_datafile = os.path.join('data','type-chart.yaml')
output_stats_datafile = os.path.join('pokemon_number_by_types.txt')

def load_data(datafile):
    with open(datafile,'r',encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        pokemons_data = [Pokemon(row) for row in csv_reader]
    return pokemons_data

def load_types_chart(datafile):
    with open(datafile,'r',encoding='utf8') as yaml_file:
        types_chart = yaml.safe_load(yaml_file)
    return types_chart

pokemons_data = load_data(pokemon_datafile)
types_chart = load_types_chart(types_chart_datafile)

def get_types_effectiveness_against_pokemon_types(types_charts,pokemon_type):
    super_effective_against = []
    not_very_effective_against = []
    no_effect_against = []

    for offensive_type,defensive_type_values in types_charts.items():
        for effectiveness_category,effectiveness_category_types in defensive_type_values.items():
            if pokemon_type in effectiveness_category_types:
                if effectiveness_category == 'super-effective':
                    super_effective_against.append(offensive_type)
                elif effectiveness_category == 'not-very-effective':
                    not_very_effective_against.append(offensive_type)
                elif effectiveness_category == 'no-effect':
                    no_effect_against.append(offensive_type)

    return super_effective_against, not_very_effective_against, no_effect_against

def check_for_type_double_in_list(list):
    type_count = {}
    for type in list:
        if type in type_count:
            type_count[type] += 1
        else:
            type_count[type] = 1
    return type_count

def calculate_final_type_chart_for_pokemon(pokemon_charts):
    if len(pokemon_charts) == 1:
        types_super_effective_against_pokemon = pokemon_charts[0][0]
        types_not_very_effective_against_pokemon = pokemon_charts[0][1]
        types_no_effect_against_pokemon = pokemon_charts[0][2]

    else:
        first_type_chart = pokemon_charts[0]
        second_type_chart = pokemon_charts[1]

        types_super_effective_against_first_type = first_type_chart[0]
        types_not_very_effective_against_first_type = first_type_chart[1]
        types_no_effect_against_first_type = first_type_chart[2]

        types_super_effective_against_second_type = second_type_chart[0]
        types_not_very_effective_against_second_type = second_type_chart[1]
        types_no_effect_against_second_type = second_type_chart[2]

        all_types_super_effective_against = types_super_effective_against_first_type + types_super_effective_against_second_type
        all_types_not_very_effective_against = types_not_very_effective_against_first_type + types_not_very_effective_against_second_type
        all_types_no_effect_against = types_no_effect_against_first_type + types_no_effect_against_second_type

        number_of_times_types_in_super_effective_list = check_for_type_double_in_list(all_types_super_effective_against)
        number_of_times_types_in_not_very_effective_list = check_for_type_double_in_list(all_types_not_very_effective_against)
        number_of_times_types_in_no_effect_list = check_for_type_double_in_list(all_types_no_effect_against)

        for super_effective_type in list(number_of_times_types_in_super_effective_list.keys()):
            for no_effect_type in list(number_of_times_types_in_no_effect_list.keys()):
                if no_effect_type == super_effective_type:
                    del number_of_times_types_in_super_effective_list[no_effect_type]

        for not_very_effective_type in list(number_of_times_types_in_not_very_effective_list.keys()):
            for no_effect_type in list(number_of_times_types_in_no_effect_list.keys()):
                if no_effect_type == not_very_effective_type:
                    del number_of_times_types_in_not_very_effective_list[no_effect_type]

        for not_very_effective_type in list(number_of_times_types_in_not_very_effective_list.keys()):
            for super_effective_type in list(number_of_times_types_in_super_effective_list.keys()):
                if not_very_effective_type == super_effective_type:
                    if number_of_times_types_in_not_very_effective_list[not_very_effective_type] == 1 and number_of_times_types_in_super_effective_list == 1:
                        del number_of_times_types_in_not_very_effective_list[not_very_effective_type]
                        del number_of_times_types_in_super_effective_list[super_effective_type]
                    elif number_of_times_types_in_not_very_effective_list == 2 and number_of_times_types_in_super_effective_list == 1:
                        del number_of_times_types_in_super_effective_list[super_effective_type]
                        number_of_times_types_in_not_very_effective_list[not_very_effective_type] -= 1
                    elif number_of_times_types_in_not_very_effective_list == 1 and number_of_times_types_in_super_effective_list == 2:
                        del number_of_times_types_in_not_very_effective_list[not_very_effective_type]
                        number_of_times_types_in_super_effective_list[super_effective_type] -= 1

        types_super_effective_against_pokemon = number_of_times_types_in_super_effective_list
        types_not_very_effective_against_pokemon = number_of_times_types_in_not_very_effective_list
        types_no_effect_against_pokemon = number_of_times_types_in_no_effect_list

    return types_super_effective_against_pokemon, types_not_very_effective_against_pokemon, types_no_effect_against_pokemon

def get_effectiveness_against_pokemon(pokemon_name):
    for pokemon in pokemons_data:
        if pokemon_name == pokemon.name:
            current_pokemon_charts = []
            for current_pokemon_type in pokemon.type1, pokemon.type2:
                if not current_pokemon_type == "":
                    super_effective_against_current_pokemon, not_very_effective_against_current_pokemon, no_effect_against_current_pokemon = get_types_effectiveness_against_pokemon_types(types_chart,current_pokemon_type)
                    current_pokemon_charts.append([super_effective_against_current_pokemon,not_very_effective_against_current_pokemon,no_effect_against_current_pokemon])
            effectiveness_charts = calculate_final_type_chart_for_pokemon(current_pokemon_charts)
            super_effective = effectiveness_charts[0]
            not_very_effective = effectiveness_charts[1]
            no_effect = effectiveness_charts[2]
            if not isinstance(super_effective, list):
                for type, number_of_times in super_effective.items():
                    if number_of_times == 1:
                        print(str(type+" deals 2x damage on "+pokemon.name))
                    elif number_of_times == 2:
                        print(str(type+" deals 4x damage on "+pokemon.name))
                for type, number_of_times in not_very_effective.items():
                    if number_of_times == 1:
                        print(str(type+" deals 1/2 damage on "+pokemon.name))
                    if number_of_times == 2:
                        print(str(type+" deals 1/4 damage on "+pokemon.name))
                for type, number_of_times in no_effect.items():
                    print(str(type+" deals no damage on "+pokemon.name))
            else:
                for type in super_effective:
                    print(str(type+"deals 2x damage on "+pokemon.name))
                for type in not_very_effective:
                    print(str(type+"deals 1/2 damage on "+pokemon.name))
                for type in no_effect:
                    print(str(type+"deals no damage on "+pokemon.name))
