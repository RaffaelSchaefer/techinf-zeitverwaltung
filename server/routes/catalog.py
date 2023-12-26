from flask import Flask
from controllers.user_controller import user_list, user_detail
from controllers.card_controller import card_list, card_detail

api = Flask(__name__)


@api.route("/users")
def users():
    return user_list()


@api.route("/user/<user_id>")
def user(user_id):
    return user_detail(user_id)


@api.route("/cards")
def cards():
    return card_list()


@api.route("/card/<card_id>")
def card(card_id):
    return card_detail(card_id)
