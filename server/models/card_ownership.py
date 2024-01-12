from src.db import create_db_connection, create_cursor, close_all


def card_ownership_create():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS card_ownership (
        user_ID  INTEGER NOT NULL,
        card_UID INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (user_ID)  REFERENCES users(ID)  ON DELETE CASCADE,
        FOREIGN KEY (card_UID) REFERENCES cards(UID) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (user_ID, card_UID)
    );
    """)
    connection.commit()
    close_all(cursor, connection)

def remove_card_ownership(card_uid):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("""
    DELETE FROM card_ownership
    WHERE card_UID = :UID;
    """, {"UID": card_uid})
    connection.commit()
    close_all(cursor, connection)

def card_ownership_delete():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("DROP TABLE card_ownership")
    connection.commit()
    close_all(cursor, connection)


def card_ownership_insert(user_ID, card_UID):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        "INSERT INTO card_ownership (user_ID, card_UID) VALUES (:user_ID, :card_UID)",
        {"user_ID": user_ID, "card_UID": card_UID}
    )
    connection.commit()
    close_all(cursor, connection)
