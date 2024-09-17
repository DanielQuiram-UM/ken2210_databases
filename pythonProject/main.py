'''
    Main logic for interacting with the database
'''
from sqlalchemy import text
from models import Pizza, Ingredient
from database import session

# Helper function to check if pizza already exists
def get_or_create_pizza(pizza_name):
    existing_pizza = session.query(Pizza).filter_by(pizza_name=pizza_name).first()
    if existing_pizza:
        return existing_pizza
    else:
        new_pizza = Pizza(pizza_name=pizza_name)
        session.add(new_pizza)
        session.commit()
        return new_pizza

# Helper function to check if ingredient already exists
def get_or_create_ingredient(ingredient_name):
    existing_ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient_name).first()
    if existing_ingredient:
        return existing_ingredient
    else:
        new_ingredient = Ingredient(ingredient_name=ingredient_name)
        session.add(new_ingredient)
        session.commit()
        return new_ingredient

# Filling the pizza table
pizzas = ["Margherita", "Marinara", "Ortolana", "Diavola", "Napolitana",
          "Calzone", "Hawaii", "Quattro Formaggi", "Vegana", "Capricciosa"]

for pizza_name in pizzas:
    get_or_create_pizza(pizza_name)

# Filling the ingredients table
ingredients = [
    "Tomato_Sauce", "Mozzarella", "Zucchini", "Eggplant", "Tomatoes",
    "Spinach", "Gorgonzola", "Parmesan", "Fontina", "Paprika", "Onion",
    "Salami", "Rocket_Salad"
]

for ingredient_name in ingredients:
    get_or_create_ingredient(ingredient_name)

# Test the connection and query the database
try:
    with session.bind.connect() as connection:
        # Simple query to test the connection
        result = connection.execute(text("SELECT 1"))
        print(result.fetchall())

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    session.close()
