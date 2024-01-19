from controller._utils import error_handling
from model import Address

@error_handling
def address_list(userID: int = None) -> dict:
    if userID is None:
        addresses = Address.get_entries()
    else:
        addresses = Address.get_user_entries(userID)
    return {
        "data": {
            "addresses": [
                {
                    "full_address": f"{address.street_name} {address.house_number} {address.town_name} {address.postal_code} {address.country}",
                    "userID": address.userID
                }
                for address in addresses
            ]
        }
    }

@error_handling
def address_detail(userID: int, index: int) -> dict:
    address = Address.get_user_entries(userID)[index]
    return {
        "data": {
            "address": {
                "full_address": f"{address.street_name} {address.house_number} {address.town_name} {address.postal_code} {address.country}",
                "street_name": address.street_name,
                "house_number": address.house_number,
                "town_name": address.town_name,
                "postal_code": address.postal_code,
                "country": address.country,
                "userID": address.userID
            }
        }
    }

@error_handling
def address_create(street_name: str, house_number: str, town_name: str, postal_code: str, country: str, userID: int) -> None:
    Address.add_entry(Address(street_name, house_number, town_name, postal_code, country, userID))

@error_handling
def address_update(
        old_street_name: str, old_house_number: str, old_town_name: str, old_postal_code: str, old_country: str, old_userID: int,
        new_street_name: str, new_house_number: str, new_town_name: str, new_postal_code: str, new_country: str, new_userID: int
) -> None:
    Address.update_entry(
        Address(old_street_name, old_house_number, old_town_name,
                old_postal_code, old_country, old_userID),
        Address(new_street_name, new_house_number, new_town_name,
                new_postal_code, new_country, new_userID)
    )

@error_handling
def address_delete(street_name: str, house_number: str, town_name: str, postal_code: str, country: str, userID: int) -> None:
    Address.delete_entry(Address(street_name, house_number, town_name, postal_code, country, userID))
