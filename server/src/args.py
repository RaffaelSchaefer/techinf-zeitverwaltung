import argparse
import click

from src.db import create_db_connection, create_cursor, close_all

parser = argparse.ArgumentParser(
    prog='Zeitverwaltung Server',
    description='includes a SQLite database and the REST API for the Project',
    epilog='Zeitverwaltung Server made with ❤️')

parser.add_argument('-r', '--reset', action='store_true',
                    help="resets the Server")
parser.add_argument('-i', '--init', action='store_true',
                    help="initializes the Server")
parser.add_argument('-add', '--add_demo_data', action='store_true',
                    help="adds Demo Data to the Project")
parser.add_argument('-d', '--debug', action='store_true',
                    help="starts the Server in debug mode")

args = parser.parse_args()


def init():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS cards (UID TEXT PRIMARY KEY NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (first_name TEXT NOT NULL, last_name TEXT NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS card_ownership (user_ID, card_ID UNIQUE, PRIMARY KEY (user_ID,card_ID))")
    close_all(cursor, connection)


def reset():
    if click.confirm('Do you want to continue?', default=True):
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute("DROP TABLE card_ownership")
        cursor.execute("DROP TABLE users")
        cursor.execute("DROP TABLE cards")
        close_all(cursor, connection)
        exit()


def add_demo_data():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute("INSERT INTO cards (UID) VALUES ('037F8B97')")
    cursor.execute(
        "INSERT INTO users (first_name, last_name) VALUES ('Max', 'Mustermann')")
    cursor.execute(
        "INSERT INTO card_ownership (user_ID, card_ID) VALUES (1, 1)")
    connection.commit()
    close_all(cursor, connection)
