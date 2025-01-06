import csv
import os
import sys
import yaml
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Pokemon:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

pokemon_datafile = resource_path(os.path.join('data','pokemon.csv'))
types_chart_datafile = resource_path(os.path.join('data','type-chart.yaml'))
img_directory_path = resource_path(os.path.join('data','img'))
ico_file_path = resource_path(os.path.join('.','pokedex.ico'))

def load_data(datafile):
    with open(resource_path(datafile),'r',encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        pokemons_data = [Pokemon(row) for row in csv_reader]
    return pokemons_data

def load_types_chart(datafile):
    with open(resource_path(datafile),'r',encoding='utf8') as yaml_file:
        types_chart = yaml.safe_load(yaml_file)
    return types_chart

def get_pokemon_names(pokemons_data):
    pokemon_names = []
    for pokemon in pokemons_data:
        pokemon_names.append(pokemon.name)
    return pokemon_names

pokemons_data = load_data(pokemon_datafile)
types_chart = load_types_chart(types_chart_datafile)
pokemon_names = get_pokemon_names(pokemons_data)

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
            pokemon_dex_number = pokemon.pokedex_number
            pokemon_image_file_name = str(pokemon_dex_number+".png")
            pokemon_image_file_path = resource_path(os.path.join(img_directory_path,pokemon_image_file_name))

            current_pokemon_charts = []

            for current_pokemon_type in pokemon.type1, pokemon.type2:
                if not current_pokemon_type == "":
                    super_effective_against_current_pokemon, not_very_effective_against_current_pokemon, no_effect_against_current_pokemon = get_types_effectiveness_against_pokemon_types(types_chart,current_pokemon_type)
                    current_pokemon_charts.append([super_effective_against_current_pokemon,not_very_effective_against_current_pokemon,no_effect_against_current_pokemon])

            effectiveness_charts = calculate_final_type_chart_for_pokemon(current_pokemon_charts)

            super_effective = effectiveness_charts[0]
            not_very_effective = effectiveness_charts[1]
            no_effect = effectiveness_charts[2]

            super_effective_string = ""
            not_very_effective_string = ""
            no_effect_string = ""
            if not isinstance(super_effective, list):
                for type, number_of_times in super_effective.items():
                    if number_of_times == 1:
                        super_effective_string += str(str(type+" deals 2x damage on "+pokemon.name+"\n"))
                    elif number_of_times == 2:
                        super_effective_string += str(str(type+" deals 4x damage on "+pokemon.name+"\n"))
                for type, number_of_times in not_very_effective.items():
                    if number_of_times == 1:
                        not_very_effective_string += str(str(type+" deals 1/2 damage on "+pokemon.name)+"\n")
                    if number_of_times == 2:
                        not_very_effective_string += str(str(type+" deals 1/4 damage on "+pokemon.name)+"\n")
                for type, number_of_times in no_effect.items():
                    no_effect_string += str(str(type+" deals no damage on "+pokemon.name)+"\n")
            else:
                for type in super_effective:
                    super_effective_string += str(str(type+" deals 2x damage on "+pokemon.name+"\n"))
                for type in not_very_effective:
                    not_very_effective_string += str(str(type+" deals 1/2 damage on "+pokemon.name)+"\n")
                for type in no_effect:
                    no_effect_string += str(str(type+" deals no damage on "+pokemon.name)+"\n")
            return pokemon_image_file_path,super_effective_string,not_very_effective_string,no_effect_string

def prepare_effectiveness_lookup(event):
    label_display_pokemon_name.config(text="")
    canvas_pokemon_image.delete("all")
    selection = combobox_pokemon_choice.get()

    if not selection == "" and not selection == None:
        label_display_pokemon_name.config(text=selection)
        pokemon_img_path, super_effective_types, not_very_effective_types, no_effect_types = get_effectiveness_against_pokemon(selection)
        pokemon_img = Image.open(resource_path(pokemon_img_path))
        pokemon_img = pokemon_img.resize((150, 150))
        pokemon_img = ImageTk.PhotoImage(pokemon_img)
        canvas_pokemon_image.create_image(0, 0, anchor='nw', image=pokemon_img)
        canvas_pokemon_image.image = pokemon_img
        if super_effective_types == "" or super_effective_types == None:
            super_effective_types = "None"
        if not_very_effective_types == "" or not_very_effective_types == None:
            not_very_effective_types = "None"
        if no_effect_types == "" or no_effect_types == None:
            no_effect_types = "None"
        effectiveness_string = "Super Effective :" + "\n" +super_effective_types + "\n\n" + "Not Very Effective :" + "\n" + not_very_effective_types + "\n\n" + "No Effect :" + "\n" + no_effect_types
        label_display_effectiveness.config(text=effectiveness_string)
        window.update_idletasks()
        current_width = window.winfo_width()
        new_height = window.winfo_reqheight()
        window.geometry(f'{current_width}x{new_height}')

window = tk.Tk()
window.title("PKMN Types")
window.geometry("400x400")
label_prompt = tk.Label(window, text="Choisir un Pokémon ci-dessous :")
label_prompt.pack(pady=10)
combobox_pokemon_choice = ttk.Combobox(window, values=pokemon_names)
combobox_pokemon_choice.current(None)
combobox_pokemon_choice.bind("<<ComboboxSelected>>", prepare_effectiveness_lookup)
combobox_pokemon_choice.pack(pady=20)
label_display_pokemon_name = tk.Label(window, text="")
label_display_pokemon_name.pack()
canvas_pokemon_image = tk.Canvas(window, width=150, height=150)
canvas_pokemon_image.pack()
label_display_effectiveness = tk.Label(window, text="")
label_display_effectiveness.pack(pady=10)
window.iconbitmap(resource_path(ico_file_path))
window.mainloop()