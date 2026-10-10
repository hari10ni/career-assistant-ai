import sqlite3

DATABASE = "database/careerpilot.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # Conversations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        title TEXT DEFAULT 'New Chat',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    # Chat History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        user_message TEXT NOT NULL,

        ai_response TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(conversation_id) REFERENCES conversations(id),

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database Initialized Successfully")


def initialize_database():
    create_tables()