'''
    All SQLAlchemy table models and association tables
'''
from sqlalchemy import Column, Integer, String, DECIMAL, Table, ForeignKey, Date, Boolean, DateTime, \
    PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# Association table to link pizzas and ingredients (many-to-many)
pizza_ingredient_association = Table(
    'pizza_ingredient', Base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.pizza_id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)
)

# Association table to link pizzas and ingredients (many-to-many)
item_ingredient_association = Table(
    'extra_item_ingredients', Base.metadata,
    Column('extra_item_id', Integer, ForeignKey('extra_items.item_id'), primary_key=True),
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
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    delivery_id = Column(Integer, ForeignKey('deliveries.delivery_id'), nullable=True)
    order_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    discount_applied = Column(Boolean, default=False)
    order_status = Column(String(50), nullable=False)

    # Define the relationship with the Customer class
    customer = relationship('Customer', backref='orders')
    delivery = relationship('Delivery', backref='orders')

# TODO: Create Table "Pizza Order"
class PizzaOrder(Base):
    __tablename__ = 'pizza_orders'

    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    pizza_id = Column(Integer, ForeignKey('pizzas.pizza_id'), nullable=False)
    pizza_amount = Column(Integer, default=1, nullable=False)

    # Composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'pizza_id'),
    )

    # Define relationships (optional)
    order = relationship('Order', backref='pizza_orders')
    pizza = relationship('Pizza', backref='pizza_orders')

# TODO: Create Table "Additional Item"
class ExtraItem(Base):
    __tablename__ = 'extra_items'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(50), nullable=False)
    cost = Column(DECIMAL(5, 2))

# TODO: Create Table "Additional Item Order"
class ExtraItemOrder(Base):
    __tablename__ = 'extra_item_orders'

    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('extra_items.item_id'), nullable=False)
    item_amount = Column(Integer, default=1, nullable=False)

    # Composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'item_id'),
    )

    # Define relationships (optional)
    order = relationship('Order', backref='extra_item_orders')
    pizza = relationship('ExtraItem', backref='extra_item_orders')

# TODO: Create Table "Delivery"
class Delivery(Base):
    __tablename__ = 'deliveries'

    delivery_id = Column(Integer, primary_key=True)
    deliverer_id = Column(Integer, ForeignKey('deliverers.deliverer_id'), nullable=False)
    initiation_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Define the relationship with the Deliverer class
    deliverer = relationship('Deliverer', backref='deliveries')

# TODO: Create Table "Deliverer"
class Deliverer(Base):
    __tablename__ = 'deliverers'
    deliverer_id = Column(Integer, primary_key=True)
    deliverer_first_name = Column(String(50), nullable=False)
    deliverer_last_name = Column(String(50), nullable=False)
    postal_code = Column(String(15), nullable=False)

# TODO: Create Table "Discount Code"
class DiscountCode(Base):
    __tablename__ = 'discount_codes'
    dicsount_code_id = Column(Integer, primary_key=True)
    discount_string = Column(String(50), nullable=False)