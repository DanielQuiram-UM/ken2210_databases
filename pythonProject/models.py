'''
    All SQLAlchemy models and association tables
'''
from sqlalchemy import Column, Integer, String, DECIMAL, Table, ForeignKey
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
