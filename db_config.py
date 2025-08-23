import mysql.connector
from utils import try_load_libmysql

try_load_libmysql()

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'omkaroptics',
    'port': 3360
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
