from dotenv import load_dotenv
import os
from application.weather import *
from application.recipes import *
from application.functions import *


def main():
    load_dotenv()  # Load the variables from .env
    spoonacular_api_key = os.getenv("SPOONACULAR_API_KEY")
    open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")

    menu_choices = (("1", "View Current Weather"),
                    ("2", "Get Recipes Based on ingredient"),
                    ("3", "Search for a recipe by keyword"),
                    ("4", "quit the application"))


    while True:
        selected_option = choice_made(menu_choices)
        if selected_option == "1":
            current_weather_data = get_current_weather_data(open_weather_api_key)
            view_current_weather_data(current_weather_data)


        elif selected_option == "2":
            raw_recipes_json = get_raw_recipes_by_ingredients(spoonacular_api_key)
            relevant_recipe_info = extract_recipe_info(raw_recipes_json)

            print_recipes(relevant_recipe_info)

            if y_or_n_choice("Would you like to get the instructions on how to cook one of the recipes? "):
                chosen_recipe_id, chosen_recipe_name = choose_recipe(relevant_recipe_info)
                get_recipe_instructions(spoonacular_api_key, chosen_recipe_id, chosen_recipe_name)

        elif selected_option == "3":
            raw_json_recipe = search_recipe_by_keyword(spoonacular_api_key)
            recipe_id, recipe_name = raw_json_recipe['results'][0]['id'], raw_json_recipe['results'][0]['title']

            get_recipe_instructions(spoonacular_api_key, recipe_id, recipe_name)

        elif selected_option == "4":
            print("Thanks for using this app! Goodbye!")
            break

        else:
            print("Please enter a valid option!")

        print("-" * 100)

if __name__ == '__main__':
    main()

