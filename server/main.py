import os
import argparse
import sqlite3
import click
import json
from flask import Flask, request, jsonify

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

if (os.path.isfile("./db.sqlite") != True):
    db = open('db.sqlite', 'x')
    db.close()


def create_db_connection(db_name="db.sqlite"):
    return sqlite3.connect("db.sqlite")


def create_cursor(connection):
    return connection.cursor()


connection = create_db_connection()
cursor = create_cursor(connection)

api = Flask(__name__)


def init():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS cards (UID TEXT PRIMARY KEY NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (first_name TEXT NOT NULL, last_name TEXT NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS card_ownership (user_ID, card_ID UNIQUE, PRIMARY KEY (user_ID,card_ID))")


def reset():
    cursor.execute("DROP TABLE card_ownership")
    cursor.execute("DROP TABLE users")
    cursor.execute("DROP TABLE cards")


def add_demo_data():
    cursor.execute("INSERT INTO cards (UID) VALUES ('037F8B97')")
    cursor.execute(
        "INSERT INTO users (first_name, last_name) VALUES ('Max', 'Mustermann')")
    cursor.execute(
        "INSERT INTO card_ownership (user_ID, card_ID) VALUES (1, 1)")
    connection.commit()


@api.route("/users")
def users():
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


def main():
    if (args.reset):
        if click.confirm('Do you want to continue?', default=True):
            reset()
            exit()
    if (args.init):
        init()
    if (args.add_demo_data):
        add_demo_data()
    cursor.close()
    connection.close()
    api.run(debug=args.debug)  # Remove Debug for later release


if __name__ == "__main__":
    main()
