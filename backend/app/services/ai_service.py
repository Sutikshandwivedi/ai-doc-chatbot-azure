import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from db import get_db_connection

# Load .env variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def get_conversation_history(session_id, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY created_at ASC
        LIMIT %s
    """, (session_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return [{"role": r["role"], "content": r["content"]} for r in rows]


def get_ai_response(session_id, user_message):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that remembers user details from previous messages."
        }
    ]

    # Inject memory
    history = get_conversation_history(session_id)
    messages.extend(history)

    # Current user message
    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages
    )

    return response.choices[0].message.content
