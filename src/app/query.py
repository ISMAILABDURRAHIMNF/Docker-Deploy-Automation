"""Query function file"""

import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def create_connection():
    """Connect to database function"""

    connection =  mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

    print("Connection Successful")
    return connection

def query_db(query, args=(), one=False):
    """Query tem"""

    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, args)

        if (
            query.strip().lower().startswith("insert")
            or query.strip().lower().startswith("update")
            or query.strip().lower().startswith("delete")
        ):
            conn.commit()

        result = cursor.fetchone() if one else cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as e:
        print(f"Error in query_db: {e}")
        return None
