from model._model import SQLiteModel


class Status:
    status: int
    userID: int

    def __init__(self, userID: int, status: int = 0) -> None:
        self.status = status
        self.userID = userID

    @staticmethod
    def create_schema() -> None:
        SQLiteModel.post("""
        CREATE TABLE IF NOT EXISTS status (
            status        INTEGER NOT NULL DEFAULT 0,
            userID        INTEGER NOT NULL PRIMARY KEY,
            FOREIGN KEY (userID) REFERENCES user(ID) ON DELETE CASCADE,
            CHECK (status IN (0, 1))
        );
        """)

    @staticmethod
    def drop_schema() -> None:
        SQLiteModel.post("DROP TABLE status")

    @staticmethod
    def add_entry(status: "Status") -> None:
        SQLiteModel.post("INSERT INTO status (status, userID) VALUES (:status, :userID)", {
            "status": status.status, "userID": status.userID
        })

    @staticmethod
    def delete_entry(status: "Status") -> None:
        SQLiteModel.post("""
            DELETE FROM status
            WHERE userID = :userID;
        """, {"userID": status.userID})

    @staticmethod
    def update_entry(old_status: "Status", new_status: "Status") -> None:
        SQLiteModel.post("""
            UPDATE status
            SET userID = :new_userID, status = :new_status
            WHERE userID = :userID;
            """, {"userID": old_status.userID, "new_userID": new_status.userID, "new_status": new_status.status})

    @staticmethod
    def get_entry(userID: int) -> "Status":
        rows = SQLiteModel.get(
            "SELECT * FROM status WHERE userID = :userID", {"userID": userID})
        return Status(*rows[0][:2]) if rows else None

    @staticmethod
    def get_entries() -> list["Status"]:
        rows = SQLiteModel.get("SELECT * FROM status")
        return [Status(*row[:2]) for row in rows]
