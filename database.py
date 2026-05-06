import mysql.connector
import os #gregado para correr el env por fuera
from dotenv import load_dotenv #gregado para correr el env por fuera

load_dotenv() #gregado para correr el env por fuera

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )