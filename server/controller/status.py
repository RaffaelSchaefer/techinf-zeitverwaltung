from controller._utils import error_handling
from model import Status


@error_handling
def status_list() -> dict:
    statuses = Status.get_entries()
    return {
        "data": {
            "statuses": [
                {
                    "status": status.status,
                    "userID": status.userID
                }
                for status in statuses
            ]
        }
    }


@error_handling
def status_detail(userID: int) -> dict:
    status = Status.get_entry(userID)
    return {
        "data": {
            "status":
                {
                    "status": status.status,
                    "userID": status.userID
                }
        }
    }


@error_handling
def status_create(userID: int, status: int = 0) -> None:
    Status.add_entry(Status(userID, status))


@error_handling
def status_update(userID: int) -> None:
    old_status = Status.get_entry(userID)
    new_status = Status(old_status.userID, 1 if old_status.status == 0 else 0)
    Status.update_entry(old_status, new_status)


@error_handling
def status_delete(userID: int) -> None:
    Status.delete_entry(Status.get_entry(userID))
