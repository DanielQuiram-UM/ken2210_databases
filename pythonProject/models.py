'''
    All SQLAlchemy table models and association tables
'''
from sqlalchemy import Column, Integer, String, DECIMAL, Table, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base

# Association table to link pizzas and ingredients (many-to-many)
pizza_ingredient_association = Table(
    'pizza_ingredient', Base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.pizza_id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)
)

# Creating the Pizza table
class Pizza(Base):
    __tablename__ = 'pizzas'
    pizza_id = Column(Integer, primary_key=True)
    pizza_name = Column(String(50))
    ingredients = relationship("Ingredient", secondary=pizza_ingredient_association, back_populates="pizzas")

# Creating the Ingredient table
class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(50))
    ingredient_cost = Column(DECIMAL(5, 2))
    dietary_status = Column(String(50))
    pizzas = relationship("Pizza", secondary=pizza_ingredient_association, back_populates="ingredients")

# TODO: Create Table "Customer"
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    customer_first_name = Column(String(50), nullable=False)
    customer_last_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String(15), nullable=False)
    # TODO: Maybe abstract the address to get to 3NF
    street = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=False)
    discount_available = Column(Boolean, default=False)
    pizza_discount_count = Column(Integer, default=0)
    password = Column(String(100), nullable=False)  # Adjust length as necessary

# TODO: Create Table "Order Information"

# TODO: Create Table "Pizza Order"

# TODO: Create Table "Additional Item"

# TODO: Create Table "Additional Item Order"

# TODO: Create Table "Delivery"

# TODO: Create Table "Delivery Personnel"

# TODO: Create Table "Discount Code"