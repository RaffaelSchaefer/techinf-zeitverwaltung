from src.db import create_db_connection, create_cursor
from models.user import user_insert


def user_list():
    try:
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        db_data = {
            "data": {
                "users": []
            }
        }
        for row in rows:
            db_data["data"]["users"].append(
                {"first_name": row[0], "last_name": row[1]})
        cursor.close()
        connection.close()
        return db_data
    except Exception as e:
        return {
            "error": str(e)
        }, 400


def user_detail(user_id):
    try:
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute("SELECT * FROM users WHERE rowid = " + user_id)
        row = cursor.fetchall()
        db_data = {
            "data": {
                "user": {
                    "first_name": row[0][0],
                    "last_name": row[0][1],
                    "cards": []
                }
            }
        }
        cursor.execute(
            "SELECT * FROM cards, card_ownership WHERE cards.rowid = card_ownership.card_ID AND card_ownership.user_ID = " + user_id)
        rows = cursor.fetchall()
        for row in rows:
            db_data["data"]["user"]["cards"].append({"UID": row[0]})
        cursor.close()
        connection.close()
        return db_data
    except Exception as e:
        return {
            "error": str(e)
        }, 400


def user_create(first_name, last_name):
    user_insert(first_name, last_name)


def user_update():
    pass


def user_delete(user_id):
    pass
