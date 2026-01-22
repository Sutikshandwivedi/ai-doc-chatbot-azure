import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            sslmode=os.getenv("POSTGRES_SSLMODE")
        )

        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        print("✅ DB CONNECTION SUCCESSFUL. Result:", result)

    except Exception as e:
        print("❌ DB CONNECTION FAILED")
        print(e)

if __name__ == "__main__":
    test_db_connection()
