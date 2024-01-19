from model._model import SQLiteModel


class User:
    id: int
    first_name: str
    last_name: str
    postionID: int

    def __init__(self, first_name: str, last_name: str, postionID: int, id: int = None) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.postionID = postionID

    @staticmethod
    def create_schema() -> None:
        SQLiteModel.post("""
            CREATE TABLE IF NOT EXISTS user (
                first_name TEXT    NOT NULL, 
                last_name  TEXT    NOT NULL,
                postionID  INTEGER NOT NULL,
                ID         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (postionID) REFERENCES position(ID)
            );
        """)

    @staticmethod
    def drop_schema() -> None:
        SQLiteModel.post("DROP TABLE user")

    @staticmethod
    def add_entry(user: "User") -> int:
        return SQLiteModel.create("""
            INSERT INTO user (first_name, last_name, postionID) 
            VALUES (:first_name, :last_name, :postionID)
        """, {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "postionID": user.postionID
        }
        )

    @staticmethod
    def delete_entry(user: "User") -> None:
        SQLiteModel.post("""
            DELETE FROM user
            WHERE ID = :ID;
        """, {"ID": user.id})

    @staticmethod
    def update_entry(old_user: "User", new_user: "User") -> None:
        SQLiteModel.post("""
            UPDATE user
            SET first_name = :first_name, last_name = :last_name, postionID = :postionID
            WHERE ID = :ID;
            """, {"first_name": new_user.first_name, "last_name": new_user.last_name, "postionID": new_user.postionID, "ID": old_user.id})

    @staticmethod
    def get_entry(ID: int) -> "User":
        rows = SQLiteModel.get(
            "SELECT * FROM user WHERE ID = :ID", {"ID": ID})
        return User(*rows[0][:4]) if rows else None

    @staticmethod
    def get_entries() -> list["User"]:
        rows = SQLiteModel.get("SELECT * FROM user")
        return [User(*row[:4]) for row in rows]
