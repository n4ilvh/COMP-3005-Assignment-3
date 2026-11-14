import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        connection = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        return connection

    except psycopg.Error as error:
        print("Database connection failed:", error)
        return None

if __name__ == "__main__":
    connection = get_connection()

    if connection:
        print("Successfully connected to PostgreSQL!")

        connection.close()
        print("Database connection closed.")