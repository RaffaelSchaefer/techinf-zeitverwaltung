from src.db import create_db_connection, create_cursor
from models.card_ownership import card_ownership_insert


def grant_card_ownership(user_ID, card_ID):
    card_ownership_insert(user_ID, card_ID)


def remove_card_ownership():
    pass
