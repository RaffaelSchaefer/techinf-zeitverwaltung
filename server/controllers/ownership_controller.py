from models.card_ownership import card_ownership_insert


def grant_card_ownership(user_ID, card_UID):
    card_ownership_insert(user_ID, card_UID)


def remove_card_ownership():
    pass
