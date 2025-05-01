import psycopg2
import os

def connect():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "store"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )