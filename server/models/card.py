card_create = """
CREATE TABLE IF NOT EXISTS cards (
    UID TEXT PRIMARY KEY NOT NULL
    )
"""

card_delete = "DROP TABLE cards"


def card_insert(UID):
    return "INSERT INTO cards (UID) VALUES ('"+UID+"')"
