import psycopg2
import os
from dotenv import load_dotenv
from PIL import Image


def create_connection():
    try:

        load_dotenv()

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT") # Default is 5432
        )
        print("####### Connected to Destination PostgreSQL successfully!")

        return conn

    except psycopg2.Error as e:
        print(f"######## Error connecting to PostgreSQL: {e}")
        conn = None

def save_image_info(name, embedding):
    conn = create_connection()
    cursr = conn.cursor()

    cursr.execute(
        "INSERT INTO pictures (name, embedding) VALUES (%s, %s) RETURNING id;",
        (name, embedding)
    )

    conn.commit()
    cursr.close()
    conn.close()

def find_closest_images(embedding):
    conn = create_connection()
    cursr = conn.cursor()

    cursr.execute(
        "SELECT id, name FROM pictures ORDER BY embedding <=> %s LIMIT 5;",
        (embedding,)
    )

    result = cursr.fetchall()
    cursr.close()
    conn.close()
    if result:
        return result
