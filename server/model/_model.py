import sqlite3


class SQLiteModel:

    @staticmethod
    def post(sql: str, arguments: dict = None, db_name: str = "db.sqlite") -> None:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        if arguments is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, arguments)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get(sql: str, arguments: dict = None, db_name: str = "db.sqlite") -> list[any]:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        if arguments is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, arguments)
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return entries

    def create(sql: str, arguments: dict, db_name: str = "db.sqlite") -> int:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        if arguments is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, arguments)
        id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        return id
