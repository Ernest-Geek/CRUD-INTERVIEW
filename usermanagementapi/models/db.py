# Database connection
import mysql.connector
from usermanagementapi.config.config import DB_CONFIG

def get_db_connection():
    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )
    return connection