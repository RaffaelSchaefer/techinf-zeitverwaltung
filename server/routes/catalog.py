from flask import Flask
from controllers.user_controller import user_list, user_detail

api = Flask(__name__)


@api.route("/users")
def users():
    return user_list()


@api.route("/user/<user_id>")
def user(user_id):
    return user_detail(user_id)
