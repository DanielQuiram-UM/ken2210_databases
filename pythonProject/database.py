'''
    This file handles database engine creation, session creation, as well as the Base class
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Creating the engine
engine = create_engine(DATABASE_URL)

# Creating a base class for declarative models
Base = declarative_base()

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()
