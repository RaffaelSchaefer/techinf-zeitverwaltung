from models.card_ownership import card_ownership_insert, remove_card_ownership


def grant_card_ownership(user_ID, card_UID):
    card_ownership_insert(user_ID, card_UID)


def card_ownership_remove(card_UID):
    remove_card_ownership(card_UID)
