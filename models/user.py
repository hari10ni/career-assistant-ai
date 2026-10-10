from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(fullname, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users(fullname, email, password)
            VALUES (?, ?, ?)
        """, (fullname, email, hashed_password))

        connection.commit()

        return True

    except Exception as e:

        print(e)

        return False

    finally:

        connection.close()

def login_user(email, password):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    if user:

        if check_password_hash(user["password"], password):

            return user

    return None