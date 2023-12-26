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


def card_detail(card_id):
    try:
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute("SELECT * FROM cards WHERE rowid = " + card_id)
        row = cursor.fetchall()
        db_data = {
            "data": {
                "card": {
                    "UID": row[0][0],
                    "OWNER_ID": {}
                }
            }
        }
        cursor.execute(
            "SELECT user_id FROM card_ownership WHERE card_ownership.card_id = " + card_id)
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


def card_delete(card_id):
    pass
