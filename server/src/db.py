import sqlite3


def create_db_connection(db_name="db.sqlite"):
    return sqlite3.connect("db.sqlite")


def create_cursor(connection):
    return connection.cursor()


def close_all(cursor, connection):
    cursor.close()
    connection.close()
