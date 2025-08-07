import psycopg2
from datetime import datetime

def store_post_analytics(conn, user_id: str, content: str):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (user_id, content, created_at) VALUES (%s, %s, %s)",
        (user_id, content, datetime.now())
    )
    conn.commit()