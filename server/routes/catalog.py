from flask import Flask, request, jsonify, redirect, url_for, render_template

from src.util import check_key
from controllers.card_controller import card_list, card_detail, card_create, toggle_card
from controllers.ownership_controller import grant_card_ownership
from controllers.user_controller import user_list, user_detail, user_create

api = Flask(__name__, template_folder="../template", static_folder="../static")
api.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')


@api.route("/")
def index():
    return redirect(url_for('site'))


@api.errorhandler(404)
def not_found(e):
    return render_template("404.pug", title="Page not found")


@api.route("/site")
def site():
    try:
        return render_template('index.pug', title="Home", user_data=user_list())
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


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
            if check_key(data["key"]) is False:
                return {"error": "Incorrect API Key"}, 401
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
            if check_key(data["key"]) is False:
                return {"error": "Incorrect API Key"}, 401
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
            if check_key(data["key"]) is False:
                return {"error": "Incorrect API Key"}, 401
            grant_card_ownership(
                data["data"]["user_ID"], data["data"]["card_UID"])
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400


@api.route("/log", methods=["POST"])
def log():
    if request.method == "POST":
        try:
            data = request.get_json()
            if check_key(data["key"]) is False:
                return {"error": "Incorrect API Key"}, 401
            toggle_card(data["data"]["UID"])
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400
