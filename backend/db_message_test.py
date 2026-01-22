import uuid
from db import get_db_connection


def test_insert_message():
    conn = None
    try:
        # 1️⃣ Connect to DB
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2️⃣ Get latest session (DICT SAFE)
        cursor.execute("""
            SELECT id
            FROM chat_sessions
            ORDER BY created_at DESC
            LIMIT 1
        """)
        session = cursor.fetchone()

        print("DEBUG session row:", session)

        if not session:
            print("❌ No session found. Run db_session_test.py first.")
            return

        # ✅ FIX HERE
        session_id = session["id"]

        # 3️⃣ Insert message
        message_id = str(uuid.uuid4())
        role = "user"
        content = "Hello, message stored correctly now"

        cursor.execute("""
            INSERT INTO chat_messages (id, session_id, role, content)
            VALUES (%s, %s, %s, %s)
        """, (message_id, session_id, role, content))

        conn.commit()

        # 4️⃣ Read message back
        cursor.execute("""
            SELECT role, content, created_at
            FROM chat_messages
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (session_id,))

        message = cursor.fetchone()

        print("✅ MESSAGE INSERTED & READ SUCCESSFULLY")
        print(message)

    except Exception as e:
        print("❌ ERROR:", e)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    test_insert_message()
