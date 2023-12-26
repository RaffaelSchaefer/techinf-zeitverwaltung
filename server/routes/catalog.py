from flask import Flask, request, jsonify
from controllers.user_controller import user_list, user_detail, user_create
from controllers.card_controller import card_list, card_detail, card_create
from controllers.ownership_controller import grant_card_ownership

api = Flask(__name__)


@api.route("/users")
def users():
    return user_list()


@api.route("/user/<user_id>")
def user(user_id):
    return user_detail(user_id)


@api.route("/create-user", methods=["POST"])
def create_user():
    if request.method == "POST":
        try:
            data = request.get_json()
            user_create(data["data"]["first_name"], data["data"]["last_name"])
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400


@api.route("/cards")
def cards():
    return card_list()


@api.route("/card/<card_id>")
def card(card_id):
    return card_detail(card_id)


@api.route("/create-card", methods=["POST"])
def create_card():
    if request.method == "POST":
        try:
            data = request.get_json()
            card_create(data["data"]["UID"])
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400


@api.route("/grant-ownership", methods=["POST"])
def grant_ownership():
    if request.method == "POST":
        try:
            data = request.get_json()
            grant_card_ownership(
                data["data"]["user_ID"], data["data"]["card_ID"])
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400
