from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

def create_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def query_db(query, args=(), one=False):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    conn.close()
    return result