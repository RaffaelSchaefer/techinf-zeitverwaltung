import os
from dotenv import load_dotenv

from routes import api
from utils import args, reset, init, add_demo_data

if not os.path.isfile("./db.sqlite"):
    db = open('db.sqlite', 'x')
    db.close()


def main():
    load_dotenv()
    if args.reset:
        reset()
    if args.init:
        init()
    if args.add_demo_data:
        add_demo_data()
    api.run(debug=args.debug, host=args.address, port=args.port)


if __name__ == "__main__":
    main()
