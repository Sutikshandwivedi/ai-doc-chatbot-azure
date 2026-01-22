import uuid
from db import get_db_connection

def test_insert_and_read_session():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        session_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO chat_sessions (id, user_name)
            VALUES (%s, %s)
            """,
            (session_id, "Sam")
        )

        cursor.execute(
            """
            SELECT id, user_name, created_at
            FROM chat_sessions
            WHERE id = %s
            """,
            (session_id,)
        )

        row = cursor.fetchone()
        conn.commit()

        print("✅ INSERT & READ SUCCESSFUL")
        print(row)

    except Exception as e:
        print("❌ DB OPERATION FAILED")
        print(e)

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    test_insert_and_read_session()
