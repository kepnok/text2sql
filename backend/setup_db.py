import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from models import Base, Employee
from database import engine, SessionLocal

def create_database_and_user():
    print("Attempting to connect to default postgres database...")
    try:
        # Try connecting as postgres user to the default postgres database
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="", host="localhost", port="5432")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("Checking if user 'my_db' exists...")
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname='my_db'")
        if not cur.fetchone():
            print("Creating user 'my_db'...")
            cur.execute("CREATE USER my_db WITH PASSWORD 'password'")
        
        print("Checking if database 'my_db' exists...")
        cur.execute("SELECT 1 FROM pg_database WHERE datname='my_db'")
        if not cur.fetchone():
            print("Creating database 'my_db'...")
            cur.execute("CREATE DATABASE my_db OWNER my_db")
            
        cur.close()
        conn.close()
        print("Database and user setup successful.")
    except Exception as e:
        print(f"Error during database/user setup (you may need to do this manually if permissions fail): {e}")

def seed_data():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    # Check if we already have data
    if db.query(Employee).count() == 0:
        print("Seeding dummy data...")
        employees = [
            Employee(first_name="John", last_name="Doe", salary=60000, department="Engineering", manager="Alice Smith"),
            Employee(first_name="Jane", last_name="Smith", salary=80000, department="Engineering", manager="Alice Smith"),
            Employee(first_name="Alice", last_name="Smith", salary=120000, department="Engineering", manager="CEO"),
            Employee(first_name="Bob", last_name="Johnson", salary=55000, department="Sales", manager="Carol White"),
            Employee(first_name="Carol", last_name="White", salary=90000, department="Sales", manager="CEO"),
        ]
        db.add_all(employees)
        db.commit()
        print("Dummy data seeded.")
    else:
        print("Data already exists. Skipping seed.")
    db.close()

if __name__ == "__main__":
    create_database_and_user()
    # Give Postgres a second to be ready with the new DB before connecting via SQLAlchemy
    import time
    time.sleep(1)
    seed_data()
