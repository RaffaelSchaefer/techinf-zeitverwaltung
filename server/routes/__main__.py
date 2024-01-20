from flask import Flask, request, jsonify, redirect, url_for, render_template

from routes._utils import check_key, page_error_handling

from controller import *

api = Flask(__name__, template_folder="../templates",
            static_folder="../static")
api.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

# Util pages


@api.errorhandler(404)
def not_found(e):
    return render_template("404.pug", title="Page not found")


@api.route("/")
def index():
    return redirect(url_for('site'))


@api.route("/site")
@page_error_handling
def site():
    return render_template('index.pug', title="Home", users=len(user_list()["data"]["users"]), cards=len(card_list()["data"]["cards"]))


# User pages


@api.route("/users")
@page_error_handling
def users():
    return render_template('users.pug', title="All Users", user_data=user_list())


@api.route("/user/<user_id>")
@page_error_handling
def user(user_id):
    return render_template('user_detail.pug', title="User Details", user_data=user_detail(user_id))


@api.route("/create-user", methods=['GET', 'POST'])
@page_error_handling
def create_user():
    if request.method == "POST":
        data = request.form
        creates_user_id = user_create(
            data["first_name"], data["last_name"], int(data["position"]))
        address_create(data["street_name"], data["house_number"], data["town_name"], data["postal_code"], data["country"], creates_user_id)
        status_create(creates_user_id)
        return redirect(url_for('users'))
    elif request.method == "GET":
        return render_template('create_user.pug', title="Create User", positions=position_list()["data"]["positions"])


@api.route("/delete-user/<user_id>", methods=["Get", "Post"])
@page_error_handling
def delete_user(user_id):
    if request.method == "POST":
        data = request.form
        if data["confirmation"] == "1":
            user_delete(user_id)
        return redirect(url_for('users'))
    elif request.method == "GET":
        return render_template('confirm.pug', title="Delete User")


@api.route("/update-user/<user_id>", methods=["Get", "Post"])
@page_error_handling
def update_user(user_id):
    address = address_detail(user_id, 0)["data"]["address"]
    if request.method == "POST":
        data = request.form
        user_update(user_id, data["first_name"],
                    data["last_name"], data["position"])
        address_update(
            address["street_name"],
            address["house_number"],
            address["town_name"],
            address["postal_code"],
            address["country"],
            user_id,
            data["street_name"],
            data["house_number"],
            data["town_name"],
            data["postal_code"],
            data["country"],
            user_id
        )
        return redirect(url_for('user', user_id=user_id))
    elif request.method == "GET":
        return render_template(
            'update_user.pug',
            title="Update User",
            user=user_detail(user_id)["data"]["user"],
            address=address,
            positions=position_list()["data"]["positions"]
        )

# Card pages


@api.route("/cards")
@page_error_handling
def cards():
    return render_template('cards.pug', title="All Cards", card_data=card_list())


@api.route("/card/<card_id>")
@page_error_handling
def card(card_id):
    return render_template('card_detail.pug', title="Card Details", card_data=card_detail(card_id), owner_detail=user_detail(card_detail(card_id)["data"]["card"]["userID"]))


@api.route("/create-card", methods=["Get", "POST"])
@page_error_handling
def create_card():
    if request.method == "POST":
        data = request.form
        card_create(data["UID"])
        return redirect(url_for('cards'))
    elif request.method == "GET":
        return render_template('create_card.pug', title="Register new Card")


@api.route("/delete-card/<card_id>", methods=["Get", "Post"])
@page_error_handling
def delete_card(card_id):
    if request.method == "POST":
        data = request.form
        if data["confirmation"] == "1":
            card_delete(card_id)
        return redirect(url_for('cards'))
    elif request.method == "GET":
        return render_template('confirm.pug', title="Delete Card")


@api.route("/update-card/<card_id>", methods=["Get", "Post"])
@page_error_handling
def update_card(card_id):
    if request.method == "POST":
        data = request.form
        card_update(card_id, data["new_id"], None)
        return redirect(url_for('card', card_id=data["new_id"]))
    elif request.method == "GET":
        return render_template('update_card.pug', title="Update Card", card_id=card_id)

# Ownership


@api.route("/grant-ownership", methods=["GET", "POST"])
@page_error_handling
def grant_ownership():
    if request.method == "POST":
        data = request.form
        card_update(data["card_UID"], data["card_UID"], data["user_ID"])
        return redirect(url_for('user', user_id=data["user_ID"]))
    elif request.method == "GET":
        return render_template('grant_ownership.pug', title="Grant Ownership", user_data=user_list(), card_data=card_list(True))


@api.route("/remove-ownership/<card_id>", methods=["GET", "POST"])
@page_error_handling
def remove_ownership(card_id):
    if request.method == "POST":
        data = request.form
        if data["confirmation"] == "1":
            card_update(card_id, card_id, None)
        return redirect(url_for('card', card_id=card_id))
    elif request.method == "GET":
        return render_template('confirm.pug', title="Remove Ownership")

# IOT Paths


@api.route("/log", methods=["POST"])
def log():
    if request.method == "POST":
        try:
            data = request.get_json()
            if check_key(data["key"]) is False:
                return {"error": "Incorrect API Key"}, 401
            status_update(
                card_detail(data["data"]["UID"])["data"]["userID"], 
                1 if status_detail(card_detail(data["data"]["UID"])["data"]["userID"]) == 0 else 0
            )
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400
