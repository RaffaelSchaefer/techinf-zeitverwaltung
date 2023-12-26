import argparse
import click

from src.db import create_db_connection, create_cursor, close_all
from models.card import card_create, card_delete, card_insert
from models.user import user_create, user_delete, user_insert
from models.card_ownership import card_ownership_create, card_ownership_delete, card_ownership_insert

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
    cursor.execute(card_create)
    cursor.execute(user_create)
    cursor.execute(card_ownership_create)
    close_all(cursor, connection)


def reset():
    if click.confirm('Do you want to continue?', default=True):
        connection = create_db_connection()
        cursor = create_cursor(connection)
        cursor.execute(card_ownership_delete)
        cursor.execute(user_delete)
        cursor.execute(card_delete)
        close_all(cursor, connection)
        exit()


def add_demo_data():
    connection = create_db_connection()
    cursor = create_cursor(connection)
    cursor.execute(card_insert("037F8B97"))
    cursor.execute(user_insert("Max", "Mustermann"))
    cursor.execute(card_ownership_insert(1, 1))
    connection.commit()
    close_all(cursor, connection)
