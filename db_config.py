import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'users',
    'port': 3360
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
