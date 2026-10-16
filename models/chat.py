
from database.db import get_connection


def save_chat(conversation_id, user_id, user_message, ai_response):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO chat_history (
                conversation_id, user_id, user_message, ai_response
            )
            VALUES (%s, %s, %s, %s)
        """, (conversation_id, user_id, user_message, ai_response))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_chat_history(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM chat_history
            WHERE user_id = %s
            ORDER BY created_at ASC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        connection.close()


def get_conversation_messages(conversation_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM chat_history
            WHERE conversation_id = %s
            ORDER BY created_at ASC
        """, (conversation_id,))

        return cursor.fetchall()

    finally:
        connection.close()


def get_recent_messages(conversation_id, limit=5):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT user_message, ai_response
            FROM chat_history
            WHERE conversation_id = %s
            ORDER BY id DESC
            LIMIT %s
        """, (conversation_id, limit))

        return list(reversed(cursor.fetchall()))

    finally:
        connection.close()


def delete_chat_history(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM chat_history
            WHERE user_id = %s
        """, (user_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_dashboard_stats(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM conversations
            WHERE user_id = %s
        """, (user_id,))

        total_conversations = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM chat_history
            WHERE user_id = %s
        """, (user_id,))

        total_messages = cursor.fetchone()[0]

        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages
        }

    finally:
        connection.close()
