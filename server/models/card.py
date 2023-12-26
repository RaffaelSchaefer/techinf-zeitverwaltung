from src.db import create_db_connection, create_cursor, close_all


def card_create():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        UID TEXT PRIMARY KEY NOT NULL
        )
    """)
    connection.commit()
    close_all(cursor, connection)


def card_delete():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("DROP TABLE cards")
    connection.commit()
    close_all(cursor, connection)


def card_insert(UID):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("INSERT INTO cards (UID) VALUES ('"+UID+"')")
    connection.commit()
    close_all(cursor, connection)
