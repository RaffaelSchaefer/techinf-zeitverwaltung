import argparse

import click

from model import *

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
    Position.create_schema()
    User.create_schema()
    Address.create_schema()
    Status.create_schema()
    Card.create_schema()
    Log.create_schema()
    exit()


def reset():
    if click.confirm('Do you want to continue?', default=True):
        Log.drop_schema()
        Card.drop_schema()
        Status.drop_schema()
        Address.drop_schema()
        User.drop_schema()
        Position.drop_schema()
        exit()


def add_demo_data():
    Position.add_entry(Position("Fullstack Developer"))
    Position.add_entry(Position("Hardware Developer"))
    User.add_entry(User("Raffael", "Schäfer", 1))
    User.add_entry(User("Florian", "Wittmann", 2))
    Address.add_entry(Address(
        "Campusallee",
        "9906C",
        "Hoppstädten-Weiersbach",
        "55768",
        "Germany",
        1
    ))
    Status.add_entry(Status(1))
    Status.add_entry(Status(2))
    Card.add_entry(Card("83451ba", 1))
    Card.add_entry(Card("37f8b97", 2))
    exit()
