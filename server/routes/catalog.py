from flask import Flask, request, jsonify, redirect, url_for, render_template

from src.util import check_key
from controllers.card_controller import card_list, card_detail, card_create, toggle_card
from controllers.ownership_controller import grant_card_ownership
from controllers.user_controller import user_list, user_detail, user_create

api = Flask(__name__, template_folder="../template", static_folder="../static")
api.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')


@api.errorhandler(404)
def not_found():
    return render_template("404.pug", title="Page not found")


@api.route("/")
def index():
    return redirect(url_for('site'))


@api.route("/site")
def site():
    try:
        return render_template('index.pug', title="Home")
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/users")
def users():
    try:
        return render_template('users.pug', title="All Users", user_data=user_list())
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/user/<user_id>")
def user(user_id):
    try:
        return render_template('user_detail.pug', title="User Details", user_data=user_detail(user_id))
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/create-user", methods=['GET', 'POST'])
def create_user():
    try:
        if request.method == "POST":
            data = request.form
            user_create(data["first_name"], data["last_name"])
            return redirect(url_for('users'))
        elif request.method == "GET":
            return render_template('create_user.pug', title="Create User")
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/cards")
def cards():
    try:
        return render_template('cards.pug', title="All Cards", card_data=card_list())
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/card/<card_id>")
def card(card_id):
    try:
        return render_template('card_detail.pug', title="Card Details", card_data=card_detail(card_id))
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/create-card", methods=["Get", "POST"])
def create_card():
    try:
        if request.method == "POST":
            data = request.form
            card_create(data["UID"])
            return redirect(url_for('cards'))
        elif request.method == "GET":
            return render_template('create_card.pug', title="Register new Card")
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/grant-ownership", methods=["GET", "POST"])
def grant_ownership():
    try:
        if request.method == "POST":
            data = request.form
            grant_card_ownership(data["user_ID"], data["card_UID"])
            return redirect(url_for('user', user_id=data["user_ID"]))
        elif request.method == "GET":
            return render_template('grant_ownership.pug', title="Grant Ownership", user_data=user_list(), card_data=card_list())
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


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
