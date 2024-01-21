from model._model import SQLiteModel


class Position:

    name: str
    id: int

    def __init__(self, name, id: int = None) -> None:
        self.name = name
        self.id = id

    @staticmethod
    def create_schema() -> None:
        SQLiteModel.post("""
        CREATE TABLE IF NOT EXISTS position (
            name TEXT    NOT NULL UNIQUE,
            ID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
        );
        """)

    @staticmethod
    def drop_schema() -> None:
        SQLiteModel.post("DROP TABLE position")

    @staticmethod
    def add_entry(position: "Position") -> None:
        SQLiteModel.post("INSERT INTO position (name) VALUES (:name)", {
            "name": position.name
        })

    @staticmethod
    def delete_entry(position: "Position") -> None:
        SQLiteModel.post("""
            DELETE FROM position
            WHERE ID = :ID;
        """, {"ID": position.id})

    @staticmethod
    def update_entry(old_position: "Position", new_position: "Position") -> None:
        SQLiteModel.post("""
            UPDATE position
            SET name = :new_name
            WHERE ID = :ID;
            """, {"ID": old_position.id, "new_name": new_position.name})

    @staticmethod
    def get_entry(id: int) -> "Position":
        rows = SQLiteModel.get(
            "SELECT * FROM position WHERE ID = :ID", {"ID": id})
        return Position(*rows[0][:2]) if rows else None

    @staticmethod
    def get_entries() -> list["Position"]:
        rows = SQLiteModel.get("SELECT * FROM position")
        return [Position(*row[:2]) for row in rows]
