# for organization purposes , we have put all the lists in here
import random

from pythonProject.database import init_db
from pythonProject.main_functions import get_or_create_pizza, get_or_create_ingredient, match_ingredients_to_pizza, \
    get_or_create_deliverer, get_or_create_extra_item
from pythonProject.models import Deliverer


def populate_data():
    # Filling in the pizza table
    pizzas = ["Margherita", "Marinara", "Ortolana", "Diavola", "Napolitana",
              "Calzone", "Hawaii", "Quattro Formaggi", "Vegana", "Capricciosa"]

    # Create for loop to ensure that all pizzas in the list are checked
    for pizza_name in pizzas:
        get_or_create_pizza(pizza_name)

    # Filling in the ingredients table
    ingredients = [
        {"ingredient_name": "Pizza Dough", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
        {"ingredient_name": "Tomato Sauce", "ingredient_cost": 2.00, "dietary_status": "vegan"},
        {"ingredient_name": "Mozzarella", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
        {"ingredient_name": "Zucchini", "ingredient_cost": 1.00, "dietary_status": "vegan"},
        {"ingredient_name": "Eggplant", "ingredient_cost": 1.00, "dietary_status": "vegan"},
        {"ingredient_name": "Gorgonzola", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
        {"ingredient_name": "Parmesan", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
        {"ingredient_name": "Fontina", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
        {"ingredient_name": "Paprika", "ingredient_cost": 1.00, "dietary_status": "vegan"},
        {"ingredient_name": "Onion", "ingredient_cost": 0.50, "dietary_status": "vegan"},
        {"ingredient_name": "Salami", "ingredient_cost": 3.00, "dietary_status": "non-vegetarian"},
        {"ingredient_name": "Rocket Salad", "ingredient_cost": 1.00, "dietary_status": "vegan"},
        {"ingredient_name": "Garlic", "ingredient_cost": 0.50, "dietary_status": "vegan"},
        {"ingredient_name": "Anchovies", "ingredient_cost": 3.00, "dietary_status": "non-vegetarian"},
        {"ingredient_name": "Capers", "ingredient_cost": 1.00, "dietary_status": "vegan"},
        {"ingredient_name": "Ham", "ingredient_cost": 3.00, "dietary_status": "non-vegetarian"},
        {"ingredient_name": "Mushrooms", "ingredient_cost": 1.50, "dietary_status": "vegan"},
        {"ingredient_name": "Pineapple", "ingredient_cost": 1.50, "dietary_status": "vegan"},
        {"ingredient_name": "Artichokes", "ingredient_cost": 1.50, "dietary_status": "vegan"}
    ]

    # For loop to check that all ingredients in the list are added/in the db
    for ingredient in ingredients:
        get_or_create_ingredient(ingredient)

    # Mapping the relations between the pizzas and their corresponding ingredients
    pizza_ingredient_map = {
        "Margherita": ["Pizza Dough", "Tomato Sauce", "Mozzarella"],
        "Marinara": ["Pizza Dough", "Tomato Sauce", "Garlic", "Onion"],
        "Ortolana": ["Pizza Dough", "Tomato Sauce", "Zucchini", "Eggplant", "Paprika"],
        "Diavola": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Salami"],
        "Napolitana": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Anchovies", "Capers"],
        "Calzone": ["Pizza Dough", "Mozzarella", "Ham", "Mushrooms", "Tomato Sauce"],
        "Hawaii": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Ham", "Pineapple"],
        "Quattro Formaggi": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Gorgonzola", "Parmesan", "Fontina"],
        "Vegana": ["Pizza Dough", "Tomato Sauce", "Zucchini", "Paprika", "Mushrooms", "Rocket Salad"],
        "Capricciosa": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Ham", "Mushrooms", "Artichokes"]
    }

    # Create for-loop to iterate through pizza map
    for pizza_name, ingredient_names in pizza_ingredient_map.items():
        match_ingredients_to_pizza(pizza_name, ingredient_names)

    # Filling in the extra items table
    #TODO: do we still need this if i create the map below?
    extra_items = [
        {"item_name": "Coca-Cola", "cost": 3.00, "dietary_status": "vegan"},
        {"item_name": "Ice Tea", "cost": 3.00, "dietary_status": "vegan"},
        {"item_name": "White Wine", "cost": 4.00, "dietary_status": "vegan"},
        {"item_name": "Red Wine", "cost": 4.00, "dietary_status": "vegan"},
        {"item_name": "Homemade Lemonade", "cost": 3.50, "dietary_status": "vegan"},
        {"item_name": "Tiramisu", "cost": 5.00, "dietary_status": "vegetarian"},
        {"item_name": "Nutella Pizza", "cost": 5.00, "dietary_status": "vegan"}
        ]

    for item_name in extra_items:
        get_or_create_extra_item(item_name)

    deliverers = [
        {"deliverer_first_name": "Anne", "deliverer_last_name": "Chovy"},
        {"deliverer_first_name": "Tony", "deliverer_last_name": "Tomato"},
        {"deliverer_first_name": "Bella", "deliverer_last_name": "Basil"},
        {"deliverer_first_name": "Marina", "deliverer_last_name": "Marinara"},
        {"deliverer_first_name": "Vito", "deliverer_last_name": "Vegano"}
    ]

    for deliverer in deliverers:
        get_or_create_deliverer(deliverer)

#TODO: CREATE EXTRA_ITEM_COST MAP

if __name__ == '__main__':
    init_db()
    populate_data()