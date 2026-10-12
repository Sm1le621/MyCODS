import psycopg

def connect_to_database():
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg.connect(
            dbname="some-postgres",
            user="postgres",
            password="6210",
            host="localhost",
            port="5432"
        )
        print("Connection to the database was successful.")
        return connection
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None