
from database.db import get_connection


def create_conversation(user_id, title="New Chat"):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO conversations (user_id, title)
            VALUES (%s, %s)
            RETURNING id
        """, (user_id, title))

        conversation_id = cursor.fetchone()["id"]
        connection.commit()

        return conversation_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_user_conversations(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM conversations
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        connection.close()


def delete_conversation(conversation_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM conversations
            WHERE id = %s
        """, (conversation_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def update_conversation_title(conversation_id, title):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE conversations
            SET title = %s
            WHERE id = %s
        """, (title, conversation_id))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_conversation(conversation_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM conversations
            WHERE id = %s
        """, (conversation_id,))

        return cursor.fetchone()

    finally:
        connection.close()


def generate_title(question):
    question = question.lower()

    if "data scientist" in question:
        return "Data Science Career"
    elif "resume" in question:
        return "Resume Review"
    elif "interview" in question:
        return "Interview Preparation"
    elif "python" in question:
        return "Python Learning Roadmap"
    elif "machine learning" in question:
        return "Machine Learning"
    elif "ai" in question:
        return "Artificial Intelligence"
    else:
        return question[:30]
