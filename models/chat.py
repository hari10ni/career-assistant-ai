from database.db import get_connection


def save_chat(
    conversation_id,
    user_id,
    user_message,
    ai_response
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (
            conversation_id,
            user_id,
            user_message,
            ai_response
        )
        VALUES (?, ?, ?, ?)
    """, (
        conversation_id,
        user_id,
        user_message,
        ai_response
    ))

    connection.commit()
    connection.close()


def get_chat_history(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM chat_history
        WHERE user_id=?
        ORDER BY created_at ASC
    """, (user_id,))

    chats = cursor.fetchall()

    connection.close()

    return chats

def get_conversation_messages(conversation_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM chat_history
        WHERE conversation_id=?
        ORDER BY created_at ASC
    """, (conversation_id,))

    chats = cursor.fetchall()

    connection.close()

    return chats

def get_recent_messages(conversation_id, limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_message, ai_response
        FROM chat_history
        WHERE conversation_id=?
        ORDER BY id DESC
        LIMIT ?
    """, (conversation_id, limit))

    messages = cursor.fetchall()

    connection.close()

    return list(reversed(messages))

def delete_chat_history(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM chat_history
        WHERE user_id=?
    """, (user_id,))

    connection.commit()
    connection.close()

def get_dashboard_stats(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM conversations
        WHERE user_id=?
    """, (user_id,))

    total_conversations = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM chat_history
        WHERE user_id=?
    """, (user_id,))

    total_messages = cursor.fetchone()[0]

    connection.close()

    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages
    }