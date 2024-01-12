from models.card import card_insert, remove_card, update_card
from src.db import create_db_connection, create_cursor, close_all


def card_list():
    try:
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute("SELECT * FROM cards")
        rows = cursor.fetchall()
        db_data = {
            "data": {
                "cards": []
            }
        }
        for row in rows:
            db_data["data"]["cards"].append(
                {"UID": row[0]})
        close_all(cursor, connection)
        return db_data
    except Exception as e:
        return {
            "error": str(e)
        }, 400

def available_cards():
    try:
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute("""
        SELECT * FROM cards
        WHERE UID NOT IN (SELECT card_UID FROM card_ownership);
        """)
        rows = cursor.fetchall()
        db_data = {
            "data": {
                "cards": []
            }
        }
        for row in rows:
            db_data["data"]["cards"].append(
                {"UID": row[0]})
        close_all(cursor, connection)
        return db_data
    except Exception as e:
        return {
            "error": str(e)
        }, 400

def card_detail(card_UID):
    try:
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute(
            "SELECT * FROM cards WHERE UID = :card_UID", {"card_UID": card_UID})
        row = cursor.fetchall()
        db_data = {
            "data": {
                "card": {
                    "UID": row[0][0],
                    "OWNER_ID": None
                }
            }
        }
        cursor.execute(
            "SELECT user_id FROM card_ownership WHERE card_ownership.card_UID = :card_UID",
            {"card_UID": card_UID}
        )
        rows = cursor.fetchall()
        for row in rows:
            db_data["data"]["card"]["OWNER_ID"] = row[0]
        close_all(cursor, connection)
        return db_data
    except Exception as e:
        return {
            "error": str(e)
        }, 400


def toggle_card(UID):
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute(
        """
        UPDATE users
        SET    logged_in = CASE WHEN logged_in = 0 THEN 1
                                ELSE 0
                            END
        FROM  card_ownership
        WHERE users.ID = card_ownership.user_ID
        AND card_ownership.card_UID = :UID;
        """, {"UID": UID}
    )
    connection.commit()
    close_all(cursor, connection)


def card_create(UID):
    card_insert(UID)


def card_update(new_uid, card_uid):
    update_card(new_uid, card_uid)


def card_delete(UID):
    remove_card(UID)
