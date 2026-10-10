import markdown
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from services.gemini_service import ask_gemini
from models.chat import (
    save_chat,
    get_chat_history,
    get_conversation_messages,
    get_recent_messages
)
from models.conversation import (
    create_conversation,
    get_user_conversations,
    update_conversation_title,
    get_conversation,
    generate_title
)

chat = Blueprint("chat", __name__)


@chat.route("/chat")
def chat_page():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conversations = get_user_conversations(
        session["user_id"]
    )

    if len(conversations) == 0:

        conversation_id = create_conversation(
            session["user_id"]
        )

        conversations = get_user_conversations(
            session["user_id"]
        )

    chat_history = get_chat_history(
        session["user_id"]
    )


    return render_template(
        "chat.html",
        username=session["user_name"],
        chats=chat_history,
        conversations=conversations,
        active_conversation=session.get("conversation_id")
    )

@chat.route("/new-chat")
def new_chat():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    create_conversation(
        session["user_id"]
    )

    return redirect(url_for("chat.chat_page"))

@chat.route("/conversation/<int:conversation_id>")
def open_conversation(conversation_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    session["conversation_id"] = conversation_id

    conversations = get_user_conversations(
        session["user_id"]
    )

    chats = get_conversation_messages(
        conversation_id
    )

    

    return render_template(
        "chat.html",
        username=session["user_name"],
        chats=chats,
        conversations=conversations,
        active_conversation=conversation_id
    )

@chat.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("message")

    conversation_id = session.get("conversation_id")

    history = ""

    if conversation_id:

        previous_messages = get_recent_messages(
            conversation_id
        )

        for msg in previous_messages:

            history += f"""
    User: {msg['user_message']}
    Assistant: {msg['ai_response']}
    """

    answer = ask_gemini(
        question,
        history
    )

    if "user_id" in session:
        conversation_id = session.get(
            "conversation_id"
        )
    
        if not conversation_id:

            conversations = get_user_conversations(
                session["user_id"]
            )

            conversation_id = conversations[0]["id"]

        conversation = get_conversation(
            conversation_id
        )

        if conversation["title"] == "New Chat":

            title = generate_title(
                question
            )

            update_conversation_title(
                conversation_id,
                title
            )

        save_chat(
            conversation_id,
            session["user_id"],
            question,
            answer
        )

    return jsonify({
        "response": answer
    })

@chat.route("/test-history")
def test_history():

    chats = get_chat_history(
        session["user_id"]
    )

    return f"Total Chats: {len(chats)}"