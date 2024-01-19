from model._model import SQLiteModel


class Log:
    time: int
    cardUID: str
    status: int
    userID: int

    def __init__(self, time: int, cardUID: str, status: int, userID: int) -> None:
        self.time = time
        self.cardUID = cardUID
        self.status = status
        self.userID = userID

    @staticmethod
    def create_schema() -> None:
        SQLiteModel.post("""
        CREATE TABLE IF NOT EXISTS log (
            time         INTEGER NOT NULL,
            cardUID      TEXT    NOT NULL,
            status       INTEGER NOT NULL,
            userID       INTEGER NOT NULL,
            FOREIGN KEY (cardUID)  REFERENCES card(UID) ON UPDATE CASCADE,
            FOREIGN KEY (status)   REFERENCES status(status),
            FOREIGN KEY (userID)   REFERENCES user(ID) ON DELETE CASCADE,
            PRIMARY KEY (time, cardUID, status, userID)
        );
        """)

    @staticmethod
    def drop_schema() -> None:
        SQLiteModel.post("DROP TABLE log")

    @staticmethod
    def add_entry(log: "Log") -> None:
        SQLiteModel.post("INSERT INTO log (time, cardUID, status, userID) VALUES (:time, :cardUID, :status, :userID)", {
            "time": log.time,
            "cardUID": log.cardUID,
            "status": log.status,
            "userID": log.userID
        })

    @staticmethod
    def delete_entry(log: "Log") -> None:
        SQLiteModel.post("""
            DELETE FROM log
            WHERE userID = :userID AND time = :time AND status = :status AND cardUID = :cardUID;
        """, {"userID": log.userID, "time": log.time, "status": log.status, "cardUID": log.cardUID})

    def update_entry(old_log: "Log", new_log: "Log") -> None:
        SQLiteModel.post("""
            Update log
            SET userID = :new_userID, time = :new_time, status = :new_status, cardUID = :new_cardUID
            WHERE userID = :userID AND time = :time AND status = :status AND cardUID = :cardUID;
        """, {
            "userID": old_log.userID,
            "time": old_log.time,
            "status": old_log.status,
            "cardUID": old_log.cardUID,
            "new_userID": new_log.userID,
            "new_time": new_log.time,
            "new_status": new_log.status,
            "new_cardUID": new_log.cardUID
        })

    @staticmethod
    def get_entries(userID: int) -> list["Log"]:
        rows = SQLiteModel.get(
            "SELECT * FROM log WHERE userID = :userID", {"userID": userID})
        return [Log(*row[:4]) for row in rows]

    # FIXME Edge Cases
    @staticmethod
    def get_entry(userID: int, time: int) -> "Log":
        row = SQLiteModel.get(
            "SELECT * FROM log WHERE userID = :userID AND time = :time", {"userID": userID, "time": time})
        return Log(*row[0][:4]) if row else None

    @staticmethod
    def get_user_entries(userID: int) -> list["Log"]:
        rows = SQLiteModel.get(
            "SELECT * FROM log WHERE userID = :userID", {"userID": userID})
        return [Log(*row[:4]) for row in rows]

    @staticmethod
    def get_entries() -> list["Log"]:
        rows = SQLiteModel.get("SELECT * FROM log ")
        return [Log(*row[:4]) for row in rows]
