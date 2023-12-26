card_ownership_create = """
CREATE TABLE IF NOT EXISTS card_ownership (
    user_ID, 
    card_ID UNIQUE, 
    PRIMARY KEY (user_ID,card_ID)
    )
"""
card_ownership_delete = "DROP TABLE card_ownership"


def card_ownership_insert(user_ID, card_ID):
    return "INSERT INTO card_ownership (user_ID, card_ID) VALUES ("+str(user_ID)+", "+str(card_ID)+")"
