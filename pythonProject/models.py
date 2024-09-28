'''
    All SQLAlchemy table models and association tables
'''
from sqlalchemy import Column, Integer, String, DECIMAL, Table, ForeignKey, Date, Boolean, DateTime, \
    PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from pythonProject.database import Base
from datetime import datetime

# Creating the junction table to link pizzas and ingredients (many-to-many)
pizza_ingredient_association = Table(
    'pizza_ingredient', Base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.pizza_id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)
)
# Creating the pizza table
class Pizza(Base):
    __tablename__ = 'pizzas'
    pizza_id = Column(Integer, primary_key=True)
    pizza_name = Column(String(50))
    ingredients = relationship("Ingredient", secondary=pizza_ingredient_association, back_populates="pizzas")

# Creating the ingredient table
class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(50), nullable=False)
    ingredient_cost = Column(DECIMAL(5, 2))
    dietary_status = Column(String(50))
    pizzas = relationship("Pizza", secondary=pizza_ingredient_association, back_populates="ingredients")

# Creating the pizza suborder table
class PizzaOrder(Base):
    __tablename__ = 'pizza_orders'
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    pizza_id = Column(Integer, ForeignKey('pizzas.pizza_id'), nullable=False)
    pizza_amount = Column(Integer, default=1, nullable=False)

# Composite primary keys in joins table (so using 2 foreign keys)
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'pizza_id'),
    )

# Defining one-many relationships
    order = relationship('Order', back_populates='pizza_orders')
    pizza = relationship('Pizza', backref='pizza_orders')

#Creating the extra item table
class ExtraItem(Base):
    __tablename__ = 'extra_items'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(50), nullable=False)
    cost = Column(DECIMAL(5, 2))
    dietary_status = Column(String(50))

# Association table to link extra items and ingredients (many-to-many)
item_ingredient_association = Table(
    'extra_item_ingredients', Base.metadata,
    Column('extra_item_id', Integer, ForeignKey('extra_items.item_id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)
)

#Creating the extra items suborder table
class ExtraItemOrder(Base):
    __tablename__ = 'extra_item_orders'
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('extra_items.item_id'), nullable=False)
    item_amount = Column(Integer, default=1, nullable=False)

# Composite primary key for the extra item order junction table
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'item_id'),
    )

 # Defining the one-many relationships
    order = relationship('Order', back_populates='extra_item_orders')
    pizza = relationship('ExtraItem', backref='extra_item_orders')

# Creating the customer table
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    customer_first_name = Column(String(50), nullable=False)
    customer_last_name = Column(String(50), nullable=False)
    customer_email = Column(String(50), nullable=False, unique =True) #=username of customer
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String(15), nullable=False)
    discount_available = Column(Boolean, default=False)
    password = Column(String(100), nullable=False)

class Customer_Address(Base):
    __tablename__ = 'customer_address'
    address_id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=False)

# Creating the order information table
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    delivery_id = Column(Integer, ForeignKey('deliveries.delivery_id'), nullable=True)
    order_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    discount_applied = Column(Boolean, default=False)
    order_status = Column(String(50), nullable=False)

    # Defining the one-to-many relationship with the customer & delivery class
    customer = relationship('Customer', backref='orders')
    delivery = relationship('Delivery', backref='orders')

    # Defining the child relations
    pizza_orders = relationship('PizzaOrder', back_populates='order', cascade="all, delete-orphan")
    extra_item_orders = relationship('ExtraItemOrder', back_populates='order', cascade="all, delete-orphan")

#Creating the delivery table
class Delivery(Base):
    __tablename__ = 'deliveries'
    delivery_id = Column(Integer, primary_key=True)
    deliverer_id = Column(Integer, ForeignKey('deliverers.deliverer_id'), nullable=False)
    initiation_time = Column(DateTime, default=datetime.utcnow, nullable=False)

#Define the relationship with the Deliverer class
    deliverer = relationship('Deliverer', backref='deliveries')

#Creating the deliverer table
class Deliverer(Base):
    __tablename__ = 'deliverers'
    deliverer_id = Column(Integer, primary_key=True)
    deliverer_first_name = Column(String(50), nullable=False)
    deliverer_last_name = Column(String(50), nullable=False)
    postal_code = Column(String(15), nullable=False)

#Creating the discount table
class DiscountCode(Base):
    __tablename__ = 'discount_codes'
    dicsount_code_id = Column(Integer, primary_key=True)
    discount_string = Column(String(50), nullable=False)