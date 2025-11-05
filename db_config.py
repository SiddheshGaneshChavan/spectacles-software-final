import mysql.connector
from utils import try_load_libmysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root@123',
    'database': 'omkaroptics',
    'port': 3360
}

def get_connection():
    try_load_libmysql
    return mysql.connector.connect(**DB_CONFIG)
