'''
    Configuration file for database settings
'''

USERNAME = 'root'
PASSWORD = 'SQLmerel9'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'pizza_delivery_system'

# Creating the database URL
DATABASE_URL = f"mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
