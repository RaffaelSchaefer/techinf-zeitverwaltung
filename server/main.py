import os

from routes.catalog import api
from src.args import args, reset, init, add_demo_data

if not os.path.isfile("./db.sqlite"):
    db = open('db.sqlite', 'x')
    db.close()


def main():
    if args.reset:
        reset()
    if args.init:
        init()
    if args.add_demo_data:
        add_demo_data()
    api.run(debug=args.debug)


if __name__ == "__main__":
    main()
