from src.db import create_db_connection, create_cursor
from models.card import card_insert


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
        cursor.close()
        connection.close()
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
        cursor.close()
        connection.close()
        return db_data
    except Exception as e:
        return {
            "error": str(e)
        }, 400


def card_create(UID):
    card_insert(UID)


def card_update():
    pass


def card_delete():
    pass
