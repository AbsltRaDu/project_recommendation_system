import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn


def log_interaction(user_id, course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO interactions (user_id, course_id) VALUES (%s, %s)",
        (user_id, course_id)
    )
    conn.commit()
    cursor.close()
    conn.close()


    