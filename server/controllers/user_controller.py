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
                {
                    "ID": row[0],
                    "first_name": row[1],
                    "last_name": row[2]
                }
            )
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
        cursor.execute(
            "SELECT * FROM users WHERE rowid = :user_id", {"user_id": user_id})
        row = cursor.fetchall()
        db_data = {
            "data": {
                "user": {
                    "ID": row[0][0],
                    "first_name": row[0][1],
                    "last_name": row[0][2],
                    "cards": []
                }
            }
        }
        cursor.execute(
            "SELECT * FROM cards, card_ownership WHERE cards.UID= card_ownership.card_UID AND card_ownership.user_ID = :user_id",
            {"user_id": user_id}
        )
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


def user_delete():
    pass
