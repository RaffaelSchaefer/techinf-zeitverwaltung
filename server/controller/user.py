from controller._utils import error_handling
from model import User, Position, Status, Card, Address


@error_handling
def user_list() -> dict:
    return {
        "data": {
            "users": [
                {
                    "ID": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "position_id": user.postionID
                }
                for user in User.get_entries()
            ]
        }
    }


@error_handling
def user_detail(userID: int) -> dict:
    user = User.get_entry(userID)
    position = Position.get_entry(user.postionID)
    status = Status.get_entry(user.id)
    cards = Card.get_user_entries(user.id)
    addresses = Address.get_user_entries(user.id)

    return {
        "data": {
            "user": {
                "ID": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "position": {
                    "name": position.name,
                    "id": user.postionID
                },
                "active": status.status == 1 if status else False,
                "cards": [{"UID": card.UID, "userID": user.id} for card in cards],
                "addresses": [{"full_address": f"{address.street_name} {address.house_number} {address.town_name} {address.postal_code} {address.country}"}for address in addresses]
            }
        }
    }


@error_handling
def user_create(first_name: str, last_name: str, position: int) -> int:
    return User.add_entry(User(first_name, last_name, position))


@error_handling
def user_update(userID: int, first_name: str, last_name: str, position: int) -> None:
    User.update_entry(User.get_entry(userID), User(
        first_name, last_name, position))


@error_handling
def user_delete(userID: int) -> None:
    User.delete_entry(User.get_entry(userID))
