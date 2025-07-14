import os
import psycopg2

def get_db_connection():
    """
    PUBLIC_INTERFACE
    Returns a new connection to the PostgreSQL database using environment variables.
    """
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_URL", "localhost"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )
    return conn
