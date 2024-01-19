from controller._utils import error_handling
from model import Log


@error_handling
def log_list(userID: int = None) -> dict:
    if userID is None:
        logs = Log.get_entries()
    else:
        logs = Log.get_user_entries(userID)
    return {
        "data": {
            "logs": [
                {
                    "UID": log.cardUID,
                    "ID": log.userID,
                    "time": log.time,
                    "status": log.status
                }
                for log in logs
            ]
        }
    }


@error_handling
def log_detail(userID: int, time: int) -> dict:
    log = Log.get_entry(userID, time)
    return {
        "data": {
            "log":
                {
                    "UID": log.cardUID,
                    "ID": log.userID,
                    "time": log.time,
                    "status": log.status
                }
        }
    }


@error_handling
def log_create(userID: int, cardUID: str, time: int, status: int) -> None:
    Log.add_entry(Log(time, cardUID, status, userID))


@error_handling
def log_update(userID: int, time: int, new_time: int, new_status: int, new_userID: int, new_cardUID: str) -> None:
    Log.update_entry(Log.get_entry(userID, time), Log(
        new_time, new_cardUID, new_status, new_userID))


@error_handling
def log_delete(userID: int, time: int) -> None:
    Log.delete_entry(Log.get_entry(userID, time))
