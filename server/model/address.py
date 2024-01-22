from model._model import SQLiteModel


class Address:
    street_name: str
    house_number: str
    town_name: str
    postal_code: str
    country: str
    userID: int

    def __init__(self, street_name: str, house_number: str, town_name: str, postal_code: str, country: str, userID: int) -> None:
        self.street_name = street_name
        self.house_number = house_number
        self.town_name = town_name
        self.postal_code = postal_code
        self.country = country
        self.userID = userID

    @staticmethod
    def create_schema() -> None:
        SQLiteModel.post("""
        CREATE TABLE IF NOT EXISTS address (
            street_name  TEXT    NOT NULL,
            house_number TEXT    NOT NULL,
            town_name    TEXT    NOT NULL,
            postal_code  TEXT    NOT NULL,
            country      TEXT    NOT NULL,
            userID       INTEGER NOT NULL,
            FOREIGN KEY (userID)  REFERENCES user(ID) ON DELETE CASCADE,
            PRIMARY KEY (street_name, house_number, town_name, postal_code, country, userID)
        );
        """)

    @staticmethod
    def drop_schema() -> None:
        SQLiteModel.post("DROP TABLE address")

    @staticmethod
    def add_entry(address: "Address") -> None:
        SQLiteModel.post("""
            INSERT INTO address (street_name, house_number, town_name, postal_code, country, userID) 
            VALUES (:street_name, :house_number, :town_name, :postal_code, :country, :userID)
        """, {
            "street_name": address.street_name,
            "house_number": address.house_number,
            "town_name": address.town_name,
            "postal_code": address.postal_code,
            "country": address.country,
            "userID": address.userID
        }
        )

    @staticmethod
    def delete_entry(address: "Address") -> None:
        SQLiteModel.post("""
            DELETE FROM address
            WHERE street_name = :street_name AND house_number = :house_number AND town_name = :town_name AND postal_code = :postal_code AND country = :country AND userID = :userID
        """, {
            "street_name": address.street_name,
            "house_number": address.house_number,
            "town_name": address.town_name,
            "postal_code": address.postal_code,
            "country": address.country,
            "userID": address.userID})

    @staticmethod
    def update_entry(old_address: "Address", new_address: "Address") -> None:
        SQLiteModel.post("""
            UPDATE address
            SET street_name = :new_street_name, house_number = :new_house_number, town_name = :new_town_name, postal_code = :new_postal_code, country = :new_country, userID = :new_userID
            WHERE street_name = :street_name AND house_number = :house_number AND town_name = :town_name AND postal_code = :postal_code AND country = :country AND userID = :userID
            """, {
            "street_name": old_address.street_name,
            "house_number": old_address.house_number,
            "town_name": old_address.town_name,
            "postal_code": old_address.postal_code,
            "country": old_address.country,
            "userID": old_address.userID,
            "new_street_name": new_address.street_name,
            "new_house_number": new_address.house_number,
            "new_town_name": new_address.town_name,
            "new_postal_code": new_address.postal_code,
            "new_country": new_address.country,
            "new_userID": new_address.userID
        })

    @staticmethod
    def get_user_entries(userID: int) -> list["Address"]:
        rows = SQLiteModel.get(
            "SELECT * FROM address WHERE userID = :userID", {"userID": userID})
        return [Address(*row[:6]) for row in rows]

    @staticmethod
    def get_entries() -> list["Address"]:
        rows = SQLiteModel.get("SELECT * FROM address")
        return [Address(*row[:6]) for row in rows]
