import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pythonProject.config import DATABASE_URL
from pythonProject.main_functions import process_orders, monitor_deliveries, deliver_orders

# Establish the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def monitor_orders():
    """Main monitoring function to check for orders and deliveries."""
    try:
        while True:
            session = Session()  # Create a new session each cycle
            print("Processing orders, delivering, and monitoring deliveries...")
            process_orders(session)
            deliver_orders(session)
            monitor_deliveries(session)
            session.commit()  # Commit changes to ensure they are visible
            session.close()  # Close session after operations
            time.sleep(10)  # Check every 30 seconds
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    print("Starting the monitoring service...")
    monitor_orders()
