from controller._utils import error_handling
from model import Card

@error_handling
def card_list(check: bool = False) -> dict:
    cards = Card.get_entries()
    return {
        "data": {
            "cards": [
                {
                    "UID": card.UID
                }
                for card in cards
                if card.userID is None or not check
            ]
        }
    }

@error_handling
def card_detail(UID: str) -> dict:
    card = Card.get_entry(UID)
    return {
        "data": {
            "card":
                {
                    "UID": card.UID,
                    "userID": card.userID
                }
        }
    }

@error_handling
def card_create(UID: str, userID: int = None) -> None:
    Card.add_entry(Card(UID, userID))

@error_handling
def card_update(UID: str, new_UID: str, new_userID: str) -> None:
    Card.update_entry(Card.get_entry(UID), Card(new_UID, new_userID))

@error_handling
def card_delete(UID: str) -> None:
    Card.delete_entry(Card.get_entry(UID))
