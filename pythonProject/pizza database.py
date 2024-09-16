# creating a pizza db
from sqlalchemy import create_engine, Column, Integer, String, text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = 'root'
PASSWORD = 'SQLmerel9'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'pizza_delivery_system'

# Create the database URL
DATABASE_URL = f"mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
# For mysqlclient, use: DATABASE_URL = f"mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# Define a sample model (optional, if you want to define tables)
class Pizzas(Base):
    __tablename__ = 'Pizzas'
    pizza_id = Column(Integer, primary_key=True)
    pizza_name = Column(String(50))
    ingredient_name = Column(String(50))

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

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

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

session.commit()
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

#database is created, let's make tables for the db
class Ingredients(Base):
    __tablename__ = 'Ingredients'
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(50))
    ingredient_cost = Column(DECIMAL(5,2))
    dietary_status = Column(String(50))


#filling the table with ingredients