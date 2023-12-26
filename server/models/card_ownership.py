from src.db import create_db_connection, create_cursor, close_all


def card_ownership_create():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS card_ownership (
        user_ID  INTEGER NOT NULL, 
        card_UID INTEGER NOT NULL UNIQUE, 
        FOREIGN KEY (user_ID)  REFERENCES users(ID),
        FOREIGN KEY (card_UID) REFERENCES cards(UID),
        PRIMARY KEY (user_ID, card_UID)
    );
    """)
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
    cursor.execute(
        """
        INSERT INTO card_ownership (user_ID, card_UID)
        SELECT :user_ID, :card_UID
        WHERE
            (SELECT 1 FROM users WHERE ID = :user_ID) IS NOT NULL
            AND (SELECT 1 FROM cards WHERE UID = :card_UID) IS NOT NULL;
        """,
        {"user_ID": user_ID, "card_UID": card_UID}
    )
    connection.commit()
    close_all(cursor, connection)  # TODO Add Error Message
