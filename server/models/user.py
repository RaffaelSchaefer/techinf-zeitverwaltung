from src.db import create_db_connection, create_cursor, close_all


def user_create():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        ID         INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT    NOT NULL, 
        last_name  TEXT    NOT NULL,
        logged_in  INTEGER NOT NULL DEFAULT 0,
        CHECK (logged_in IN (0, 1))
    );
    """)  # TODO Schema needs improvement
    connection.commit()
    close_all(cursor, connection)


def user_delete():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("DROP TABLE users")
    connection.commit()
    close_all(cursor, connection)


def user_insert(first_name, last_name):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute(
        "INSERT INTO users (first_name, last_name) VALUES (:first_name, :last_name)",
        {"first_name": first_name, "last_name": last_name}
    )
    connection.commit()
    close_all(cursor, connection)
