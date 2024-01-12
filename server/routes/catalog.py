from flask import Flask, request, jsonify, redirect, url_for, render_template

from src.util import check_key
from controllers.card_controller import card_list, card_detail, card_create, card_delete, toggle_card, available_cards, card_update
from controllers.ownership_controller import grant_card_ownership, card_ownership_remove
from controllers.user_controller import user_list, user_detail, user_create, user_delete, user_update

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
        return render_template('index.pug', title="Home", users=len(user_list()["data"]["users"]), cards=len(card_list()["data"]["cards"]))
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


@api.route("/delete-user/<user_id>", methods=["Get", "Post"])
def delete_user(user_id):
    try:
        if request.method == "POST":
            data = request.form
            if data["confirmation"] == "1":
                user_delete(user_id)
            return redirect(url_for('users'))
        elif request.method == "GET":
            return render_template('confirm.pug', title="Delete User")
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/update-user/<user_id>", methods=["Get", "Post"])
def update_user(user_id):
    try:
        if request.method == "POST":
            data = request.form
            user_update(data["first_name"], data["last_name"], user_id)
            return redirect(url_for('user', user_id=user_id))
        elif request.method == "GET":
            return render_template('update_user.pug', title="Update User", first_name=user_detail(user_id)["data"]["user"]["first_name"], last_name=user_detail(user_id)["data"]["user"]["last_name"])
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
        return render_template('card_detail.pug', title="Card Details", card_data=card_detail(card_id), owner_detail=user_detail(card_detail(card_id)["data"]["card"]["OWNER_ID"]))
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


@api.route("/delete-card/<card_id>", methods=["Get", "Post"])
def delete_card(card_id):
    try:
        if request.method == "POST":
            data = request.form
            if data["confirmation"] == "1":
                card_delete(card_id)
            return redirect(url_for('cards'))
        elif request.method == "GET":
            return render_template('confirm.pug', title="Delete Card")
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/update-card/<card_id>", methods=["Get", "Post"])
def update_card(card_id):
    try:
        if request.method == "POST":
            data = request.form
            card_update(data["new_id"], card_id)
            return redirect(url_for('card', card_id=data["new_id"]))
        elif request.method == "GET":
            return render_template('update_card.pug', title="Update Card", card_id=card_id)
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
            return render_template('grant_ownership.pug', title="Grant Ownership", user_data=user_list(), card_data=available_cards())
    except Exception as e:
        return render_template('error.pug', title="Error", code=400, msg=str(e))


@api.route("/remove-ownership/<card_id>", methods=["GET", "POST"])
def remove_ownership(card_id):
    try:
        if request.method == "POST":
            data = request.form
            if data["confirmation"] == "1":
                card_ownership_remove(card_id)
            return redirect(url_for('card', card_id=card_id))
        elif request.method == "GET":
            return render_template('confirm.pug', title="Remove Ownership")
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
