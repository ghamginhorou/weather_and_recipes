import requests


def get_raw_recipes_by_ingredients(api_key):
    """
    Fetches recipes based on user-provided ingredients and returns the raw API response.

    Args:
    - api_key (str): Spoonacular API key.

    Returns:
    - JSON response from the Spoonacular API.
    """

    # Get ingredients from user and add to list 'ingredients'
    ingredients = []
    ingredient = input("\nType the ingredient you want to include in the recipe or: ")
    while True:

        if not ingredients and ingredient.lower() == "q":
            print("You have not included any ingredients.")
            ingredient = input("\nPlease type at least one ingredient to search for recipes: ")
            continue
        elif ingredient == "":
            ingredient = input("\nPlease type the ingredient you want to include in the recipe or 'q' to search for recipes: ")
            continue
        elif ingredient == "q":
            break

        else:
            ingredients.append(ingredient)
            ingredient = input("\nAdd another ingredient to search for recipes, or type 'q' to start the search: ")

    # Set up the API call to Spoonacular
    base_url = "https://api.spoonacular.com/recipes/findByIngredients"

    # Parameters for the API call
    params = {
        'apiKey': api_key,
        'ingredients': ingredients,  # List of ingredients provided by user
        'number': 5,  # Number of recipes to return
        'ranking': 1,  # Rank recipes by relevance
        'ignorePantry': True  # Ignore common pantry items
    }

    try:
        # Make the API call
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        # Return the raw response
        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return None


def extract_recipe_info(raw_recipes):
    """
    Extracts relevant information from raw recipe data and returns a list of dictionaries.

    Args:
    - raw_recipes (list): The raw JSON response from the Spoonacular API.

    Returns:
    - List of dictionaries containing recipe ID, title, and all needed ingredients.
    """

    if raw_recipes:
        extracted_recipes = []
        recipe_number = 1

        for recipe in raw_recipes:
            # Create a dictionary for each recipe
            recipe_info = {
                "number": str(recipe_number),
                "id": recipe.get("id"),  # Include the recipe ID
                "name": recipe.get("title"),
                "ingredients": [],
            }

            # Combine used and missed ingredients for all needed ingredients
            all_ingredients = recipe.get("usedIngredients", []) + recipe.get("missedIngredients", [])
            for ingredient in all_ingredients:
                ingredient_info = {
                    "name": ingredient.get("name"),
                    "amount": ingredient.get("amount"),
                    "unit": ingredient.get("unit") or "",  # Handle cases where unit might be None
                }
                recipe_info["ingredients"].append(ingredient_info)

            extracted_recipes.append(recipe_info)
            recipe_number += 1
        return extracted_recipes


def print_recipes(recipes):
    """
    Prints the recipe information in a structured manner.

    Args:
    - recipes (list): A list of dictionaries containing recipe information.
    """

    for recipe in recipes:
        print(f"\nRecipe {recipe['number']}: {recipe['name']}")
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            amount = ingredient.get('amount', 0)
            unit = ingredient.get('unit', '')
            ingredient_name = ingredient.get('name', '')
            print(f"  - {amount} {unit} {ingredient_name}")
        print()


def choose_recipe(recipes):
    """
    Allows the user to choose a recipe by its number and returns the ID of the selected recipe.

    Args:
    - recipes (list): A list of dictionaries containing recipe information.

    Returns:
    - int: The ID of the selected recipe, or None if the input is invalid.
    """

    valid_numbers = [recipe['number'] for recipe in recipes]

    while True:

        choice = input("Enter the recipe number you want to get instructions for: ")

        # Check if the choice is valid
        if choice in valid_numbers:
            # Return the ID of the chosen recipe
            index = valid_numbers.index(choice)
            return recipes[index]['id'], recipes[index]['name']
        else:
            print("Please enter a valid recipe number.")


def get_recipe_instructions(api_key, recipe_id, recipe_title):
    """
    Fetches cooking instructions for a recipe based on its ID.

    Args:
    - api_key (str): The Spoonacular API key.
    - recipe_id (int): The ID of the recipe to fetch instructions for.
    - recipe_title (str): The title of the recipe for better readability.

    Returns:
    - None
    """

    instructions_url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={api_key}"

    try:
        response = requests.get(instructions_url)
        response.raise_for_status()
        instructions_data = response.json()

        if instructions_data:
            print(f"\nInstructions for {recipe_title}:")
            for instruction in instructions_data[0]['steps']:
                print(f"{instruction['number']}. {instruction['step']}")
        else:
            print(f"No instructions found for the recipe '{recipe_title}'.")
        print()
    except requests.RequestException as e:
        print(f"Error fetching instructions for '{recipe_title}': {e}")


def search_recipe_by_keyword(api_key):
    """
    Fetches recipes based on a user-provided keyword and returns the raw API response.

    Args:
    - api_key (str): Spoonacular API key.

    Returns:
    - JSON response from the Spoonacular API if successful.
    """

    query = input("\nEnter a keyword to search for recipes: ")

    while not query:
        # Prompt the user again if the input is empty
        query = input("\nPlease enter a valid keyword to search for recipes: ")

    base_url = "https://api.spoonacular.com/recipes/complexSearch"

    # Parameters for the API call
    params = {
        'apiKey': api_key,
        'query': query,  # Search keyword provided by user
        'number': 1,     # Number of recipes to return
        'addRecipeInformation': True  # Include additional recipe details
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return None