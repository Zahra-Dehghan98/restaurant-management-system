# import sql
import psycopg2
from psycopg2 import sql

# connect to database
def get_connection():
    return psycopg2.connect (
        dbname="restaurant_db",
        user="postgres",
        password="0914zahra",
        host="localhost",
        port="5432"
)

