from src.db import create_db_connection, create_cursor, close_all


def user_create():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        ID         INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT    NOT NULL, 
        last_name  TEXT    NOT NULL,
        address    TEXT    NOT NULL,
        position   TEXT    NOT NULL,
        logged_in  INTEGER NOT NULL DEFAULT 0,
        CHECK (logged_in IN (0, 1))
    );
    """)
    connection.commit()
    close_all(cursor, connection)


def remove_user(user_id):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("""
    DELETE FROM users
    WHERE ID = :user_id;
    """, {"user_id": user_id})
    connection.commit()
    close_all(cursor, connection)


def user_delete():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("DROP TABLE users")
    connection.commit()
    close_all(cursor, connection)


def user_insert(first_name, last_name, address, position):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
        INSERT INTO users (first_name, last_name, address, position) 
        VALUES (:first_name, :last_name, :address, :position)
        """, {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "position": position
    }
    )
    connection.commit()
    close_all(cursor, connection)


def update_user(first_name, last_name, address, position, user_id):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
        UPDATE users
        SET first_name = :first_name, last_name = :last_name, address = :address, position = :position
        WHERE ID = :user_id;
        """, {"first_name": first_name, "last_name": last_name, "address": address, "position": position, "user_id": user_id})
    connection.commit()
    close_all(cursor, connection)
