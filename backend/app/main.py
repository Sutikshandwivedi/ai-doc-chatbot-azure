from flask import Flask, request, jsonify, send_from_directory
from app.services.ai_service import get_ai_response
from db import (
    get_db_connection,
    get_latest_session,
    create_session,
    insert_message
)

def create_app():
    app = Flask(__name__, static_folder="../static")

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data["message"]

        conn = get_db_connection()
        cursor = conn.cursor()

        session = get_latest_session(cursor)
        if session:
            session_id = session["id"]
        else:
            session_id = create_session(cursor, user_name="Sam")

        insert_message(cursor, session_id, "user", user_message)

        ai_reply = get_ai_response(session_id, user_message)

        insert_message(cursor, session_id, "assistant", ai_reply)

        conn.commit()
        conn.close()

        return jsonify({
            "session_id": session_id,
            "ai_response": ai_reply
        })

    return app
