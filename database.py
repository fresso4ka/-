import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("expenses.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                comment TEXT DEFAULT ''
            )
        """)


def add_expense(amount, category, date, comment=""):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO expenses (amount, category, date, comment) VALUES (?, ?, ?, ?)",
            (amount, category, date, comment)
        )
        return cursor.lastrowid


def get_expenses():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, amount, category, date, comment FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def delete_expense(expense_id):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cursor.rowcount > 0


def get_total():
    with get_connection() as connection:
        row = connection.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses").fetchone()
        return round(float(row["total"]), 2)
