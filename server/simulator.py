import time
import random
import os
import requests

from controller import card_list

cards = card_list()["data"]["cards"]
UIDs = [card["UID"] for card in cards]
key = os.getenv('API_KEY')

while True:
    r = requests.post("http://localhost:9000/log", json={"key": key, "data": {"UID": random.choice(UIDs)}})
    time.sleep(60)
