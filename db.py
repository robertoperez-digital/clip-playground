import psycopg2
import requests
import torch
import clip
import array
from PIL import Image


def create_connection():
    try:

        conn = psycopg2.connect(
            host="127.0.0.1",
            database="clip_playground",
            user="admin",
            password="pass",
            port="5432" # Default is 5432
        )
        print("Connected to Destination PostgreSQL successfully!")

        return conn

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
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
