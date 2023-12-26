user_create = """
CREATE TABLE IF NOT EXISTS users (
    first_name TEXT NOT NULL, 
    last_name  TEXT NOT NULL
    )
"""

user_delete = "DROP TABLE users"


def user_insert(first_name, last_name):
    return "INSERT INTO users (first_name, last_name) VALUES ('"+first_name+"', '"+last_name+"')"
