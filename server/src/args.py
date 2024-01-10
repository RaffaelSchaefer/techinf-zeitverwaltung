import argparse

import click

from models.card import card_create, card_delete, card_insert
from models.card_ownership import card_ownership_create, card_ownership_delete, card_ownership_insert
from models.user import user_create, user_delete, user_insert

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
parser.add_argument('-a', '--address', type=str,
                    help="the ip address the server should run on", default="0.0.0.0")
parser.add_argument('-p', '--port', type=str,
                    help="the port the server should run on", default="5000")

args = parser.parse_args()


def init():
    card_create()
    user_create()
    card_ownership_create()
    exit()


def reset():
    if click.confirm('Do you want to continue?', default=True):
        card_ownership_delete()
        user_delete()
        card_delete()
        exit()


def add_demo_data():
    card_insert("83 45 1b 0a")
    card_insert("03 7f 8b 97")
    user_insert("John", "Doe")
    user_insert("Jane", "Doe")
    card_ownership_insert(1, "83 45 1b 0a")
    card_ownership_insert(2, "03 7f 8b 97")
    exit()
