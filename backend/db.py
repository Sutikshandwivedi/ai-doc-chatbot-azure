import os
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        sslmode=os.getenv("POSTGRES_SSLMODE"),
        cursor_factory=RealDictCursor
    )

def get_latest_session(cursor):
    cursor.execute("""
        SELECT id
        FROM chat_sessions
        ORDER BY created_at DESC
        LIMIT 1
    """)
    return cursor.fetchone()

def create_session(cursor, user_name="Sam"):
    session_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO chat_sessions (id, user_name)
        VALUES (%s, %s)
    """, (session_id, user_name))
    return session_id

def insert_message(cursor, session_id, role, content):
    message_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO chat_messages (id, session_id, role, content)
        VALUES (%s, %s, %s, %s)
    """, (message_id, session_id, role, content))
