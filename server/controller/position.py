from controller._utils import error_handling
from model import Position

@error_handling
def position_list() -> dict:
    positions = Position.get_entries()
    return {
        "data": {
            "positions": [
                {
                    "name": position.name,
                    "ID": position.id
                }
                for position in positions
            ]
        }
    }

@error_handling
def position_detail(ID: int) -> dict:
    position = Position.get_entry(ID)
    return {
        "data": {
            "position":
                {
                    "name": position.name,
                    "ID": position.id
                }
        }
    }

@error_handling
def position_create(name: str) -> None:
    Position.add_entry(Position(name))

@error_handling
def position_update(ID: int, new_name: str) -> None:
    Position.update_entry(Position.get_entry(ID), Position(new_name))

@error_handling
def position_delete(ID: int) -> None:
    Position.delete_entry(Position.get_entry(ID))
