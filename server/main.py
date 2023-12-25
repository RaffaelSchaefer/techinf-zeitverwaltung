import os

from routes.catalog import api
from src.db import create_db_connection, create_cursor
from src.args import args, reset, init, add_demo_data

if (os.path.isfile("./db.sqlite") != True):
    db = open('db.sqlite', 'x')
    db.close()


def main():
    if (args.reset):
        reset()
    if (args.init):
        init()
    if (args.add_demo_data):
        add_demo_data()
    api.run(debug=args.debug)  # Remove Debug for later release


if __name__ == "__main__":
    main()
