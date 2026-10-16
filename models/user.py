
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(fullname, email, password):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (fullname, email, password)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """, (fullname, email, hashed_password))

        created_user = cursor.fetchone()
        connection.commit()

        return created_user is not None

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def login_user(email, password):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            return user

        return None

    finally:
        connection.close()
