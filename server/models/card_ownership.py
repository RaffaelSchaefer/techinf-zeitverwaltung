from src.db import create_db_connection, create_cursor, close_all


def card_ownership_create():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS card_ownership (
        user_ID, 
        card_ID UNIQUE, 
        PRIMARY KEY (user_ID,card_ID)
        )
    """)
    connection.commit()
    close_all(cursor, connection)


def card_ownership_delete():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("DROP TABLE card_ownership")
    connection.commit()
    close_all(cursor, connection)


def card_ownership_insert(user_ID, card_ID):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute(
        "INSERT INTO card_ownership (user_ID, card_ID) VALUES ("+str(user_ID)+", "+str(card_ID)+")")
    connection.commit()
    close_all(cursor, connection)
