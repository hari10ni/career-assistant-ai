from database.db import get_connection


def create_conversation(user_id, title="New Chat"):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations
        (user_id, title)
        VALUES (?, ?)
    """, (user_id, title))

    connection.commit()

    conversation_id = cursor.lastrowid

    connection.close()

    return conversation_id


def get_user_conversations(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM conversations
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))

    conversations = cursor.fetchall()

    connection.close()

    return conversations


def delete_conversation(conversation_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM conversations
        WHERE id=?
    """, (conversation_id,))

    connection.commit()
    connection.close()


def update_conversation_title(conversation_id, title):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE conversations
        SET title=?
        WHERE id=?
    """, (title, conversation_id))

    connection.commit()
    connection.close()

def get_conversation(conversation_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM conversations
        WHERE id=?
    """, (conversation_id,))

    conversation = cursor.fetchone()

    connection.close()

    return conversation

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