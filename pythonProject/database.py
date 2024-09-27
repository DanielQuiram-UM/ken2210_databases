'''
    This file handles database engine creation, session creation, as well as the Base class
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pythonProject.config import DATABASE_URL

# Creating the engine
engine = create_engine(DATABASE_URL)

# Creating a base class for declarative models
Base = declarative_base()

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Function to initialize (drop and create) the tables
def init_db():
    pass
    # This is to always create the tables from scratch
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
