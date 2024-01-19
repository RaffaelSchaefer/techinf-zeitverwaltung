from model._model import SQLiteModel


class Card:
    UID: str
    userID: int

    def __init__(self, UID: str, userID: int = None) -> None:
        self.UID = UID
        self.userID = userID

    @staticmethod
    def create_schema() -> None:
        SQLiteModel.post("""
        CREATE TABLE IF NOT EXISTS card (
            UID        TEXT    NOT NULL PRIMARY KEY,
            userID     INTEGER,
            FOREIGN KEY (userID) REFERENCES user(ID)
        );
        """)

    @staticmethod
    def drop_schema() -> None:
        SQLiteModel.post("DROP TABLE card")

    def add_entry(card: "Card") -> None:
        if card.userID is None:
            SQLiteModel.post("INSERT INTO card (UID) VALUES (:UID)", {
                "UID": card.UID
            })
        else:
            SQLiteModel.post("INSERT INTO card (UID, userID) VALUES (:UID, :userID)", {
                "UID": card.UID,
                "userID": card.userID
            })

    @staticmethod
    def delete_entry(card: "Card") -> None:
        SQLiteModel.post("""
            DELETE FROM card
            WHERE UID = :UID;
        """, {"UID": card.UID})

    @staticmethod
    def update_entry(old_card: "Card", new_card: "Card") -> None:
        SQLiteModel.post("""
            UPDATE card
            SET UID = :new_uid, userID = :new_userID
            WHERE UID = :old_uid;
            """, {"new_uid": new_card.UID, "new_userID": new_card.userID, "old_uid": old_card.UID})

    @staticmethod
    def get_user_entries(userID: int) -> list["Card"]:
        rows = SQLiteModel.get(
            "SELECT * FROM card WHERE userID = :userID", {"userID": userID})
        return [Card(*row[:2]) for row in rows]

    @staticmethod
    def get_entry(UID: str) -> "Card":
        rows = SQLiteModel.get(
            "SELECT * FROM card WHERE UID = :UID", {"UID": UID})
        return Card(*rows[0][:2]) if rows else None

    @staticmethod
    def get_entries() -> list["Card"]:
        rows = SQLiteModel.get("SELECT * FROM card")
        return [Card(*row[:2]) for row in rows]
