# Creating a pizza delivery db yay!
from sqlalchemy import create_engine, Column, Integer, String, text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = 'root'
PASSWORD = 'SQLmerel9'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'pizza_delivery_system'

# Creating the database URL
DATABASE_URL = f"mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

#Creating an engine WHAT IS HAPPENING???
engine = create_engine(DATABASE_URL)

# Creating a base class for declarative models WHAT IS HAPPENING???
Base = declarative_base()

# Create tables in the database WHAT IS THIS???
Base.metadata.create_all(engine)

# Create a session factory WHAT IS THIS???
Session = sessionmaker(bind=engine)
session = Session()

##################################### THE ACTUAL FUN STUFF

# Creating our first table whoopwhoop
class Pizzas(Base):
    __tablename__ = 'Pizzas'
    pizza_id = Column(Integer, primary_key=True)
    pizza_name = Column(String(50))
    ingredient_name = Column(String(50), foreign_key=True)

#Filling the pizza table
Margherita = Pizzas(pizza_name = "Margherita")
Marinara = Pizzas(pizza_name = "Marinara")
Ortolana = Pizzas(pizza_name = "Ortolana")
Diavola = Pizzas(pizza_name = "Diavola")
Napolitana = Pizzas(pizza_name = "Napolitana")
Calzone = Pizzas(pizza_name = "Calzone")
Hawaii = Pizzas(pizza_name = "Hawaii")
Quattro_Formaggi = Pizzas(pizza_name = "Quattro Formaggi")
Vegana = Pizzas(pizza_name = "Vegana")
Capricciosa = Pizzas(pizza_name = "Capricciosa")

#Adding the pizzas to the db
session.add(Margherita)
session.add(Marinara)
session.add(Ortolana)
session.add(Diavola)
session.add(Napolitana)
session.add(Quattro_Formaggi)
session.add(Calzone)
session.add(Hawaii)
session.add(Vegana)
session.add(Capricciosa)

#the command to push it all through PROBLEM: IT ADDS THE ALREADY COMMITED ONES AGAIN AND GIVES THEM A NEW ID!!!
session.commit()

#Creating the ingredients table
class Ingredients(Base):
    __tablename__ = 'Ingredients'
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(50))
    ingredient_cost = Column(DECIMAL(5,2))
    dietary_status = Column(String(50))

#Filling the table with ingredients
Tomato_Sauce = Ingredients(ingredient_name = "Tomato_Sauce")
Mozzarella = Ingredients(ingredient_name = "Mozzarella")
Zucchini = Ingredients(ingredient_name = "Zucchini")
Eggplant = Ingredients(ingredient_name = "Eggplant")
Tomatoes = Ingredients(ingredient_name = "Tomatoes")
Spinach = Ingredients(ingredient_name = "Spinach")
Gorgonzola = Ingredients(ingredient_name = "Gorgonzola")
Parmesan = Ingredients(ingredient_name = "Parmesan")
Fontina = Ingredients(ingredient_name = "Fontina")
Paprika = Ingredients(ingredient_name = "Paprika")
Onion = Ingredients(ingredient_name = "Onion")
Salami = Ingredients(ingredient_name = "Salami")
Rocket_Salad = Ingredients(ingredient_name = "Rocket_Salad")

# Test the connection and query the database
try:
    with engine.connect() as connection:
        # Simple query to test the connection
        result = connection.execute(text("SELECT 1"))
        print(result.fetchall())

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    session.close()