from flask import Blueprint, request, jsonify
from app.services.ai_service import get_ai_response
from db import (
    get_db_connection,
    get_latest_session,
    create_session,
    insert_message,
    get_conversation_history
)

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1️⃣ Get or create session
    session = get_latest_session(cursor)

    if session:
        session_id = session["id"]
    else:
        session_id = create_session(cursor)

    # 2️⃣ Load conversation history
    history = get_conversation_history(cursor, session_id)

    # 3️⃣ Save user message
    insert_message(cursor, session_id, "user", user_message)

    # 4️⃣ AI response WITH MEMORY
    ai_response = get_ai_response(session_id, user_message)


    # 5️⃣ Save AI message
    insert_message(cursor, session_id, "assistant", ai_response)

    conn.commit()
    conn.close()

    return jsonify({
        "session_id": session_id,
        "response": ai_response
    })
