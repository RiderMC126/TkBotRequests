from aiogram.types import Message
import logging
import sqlite3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    try:
        conn = sqlite3.connect("bot/db.db")
        cursor = conn.cursor()

        # Таблица заявок
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            name TEXT,
            age TEXT,
            comment TEXT,
            status TEXT DEFAULT 'new',
            answer TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Таблица пользователей
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registered_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()
        print(f"База данных успешно создана или уже существовала.")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")

# ------------------ Работа с ботом ------------------

def add_user(user: Message):
    """Добавление пользователя в таблицу users, если его там нет"""
    conn = sqlite3.connect("bot/db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """, (user.from_user.id, user.from_user.username, user.from_user.first_name, user.from_user.last_name))
        conn.commit()
    except Exception as e:
        logger.error(f"Ошибка добавления пользователя: {e}")
    finally:
        conn.close()

def add_request(user: Message, ticket_text: str):
    """Добавление заявки в таблицу requests"""
    conn = sqlite3.connect("bot/db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO requests (user_id, username, comment)
            VALUES (?, ?, ?)
        """, (user.from_user.id, user.from_user.username, ticket_text))
        conn.commit()
    except Exception as e:
        logger.error(f"Ошибка добавления заявки: {e}")
    finally:
        conn.close()


# ------------------ Работа с Tkinter ------------------
def get_requests(status="new"):
    conn = sqlite3.connect("bot/db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, username, comment FROM requests WHERE status=?", (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def answer_request(request_id, answer_text):
    conn = sqlite3.connect("bot/db.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE requests
        SET answer = ?, status = 'answered'
        WHERE id = ?
    """, (answer_text, request_id))
    conn.commit()
    conn.close()