import time

from flask import Flask, request, jsonify, redirect, url_for, render_template
from routes._utils import check_key, page_error_handling
from controller import *

api = Flask(__name__, template_folder="../templates", static_folder="../static")
api.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

# Util pages


@api.errorhandler(404)
def not_found(e):
    return render_template("utils/404.pug", title="Page not found")


@api.route("/")
def index():
    return redirect(url_for('site'))


@api.route("/site")
@page_error_handling
def site():
    return render_template('index.pug', title="Home", log_data=log_list())


# User pages


@api.route("/users", methods=['GET', 'POST'])
@page_error_handling
def users():
    if request.method == "POST":
        data = request.form
        result = []
        for user in user_list()["data"]["users"]:
            name = f'{user["first_name"]} {user["last_name"]}'
            if data["search"] in name:
                result.append(user)
        return render_template('user/user_search.pug', title="Search Result", user_data=result)
    elif request.method == "GET":
        return render_template('user/user_list.pug', title="All Users", user_data=user_list())


@api.route("/user/<user_id>")
@page_error_handling
def user(user_id):
    return render_template('user/user_detail.pug', title="User Details", user_data=user_detail(user_id), log_data=log_list(user_id))


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
        return render_template('user/user_create.pug', title="Create User", positions=position_list()["data"]["positions"])


@api.route("/delete-user/<user_id>", methods=["Get", "Post"])
@page_error_handling
def delete_user(user_id):
    if request.method == "POST":
        data = request.form
        if data["confirmation"] == "1":
            user_delete(user_id)
        return redirect(url_for('users'))
    elif request.method == "GET":
        return render_template('utils/confirm.pug', title="Delete User")


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
            'user/user_update.pug',
            title="Update User",
            user=user_detail(user_id)["data"]["user"],
            address=address,
            positions=position_list()["data"]["positions"]
        )

# Card pages


@api.route("/cards", methods=['GET', 'POST'])
@page_error_handling
def cards():
    if request.method == "POST":
        data = request.form
        result = []
        for card in card_list()["data"]["cards"]:
            if data["search"] in card["UID"]:
                result.append(card)
        return render_template('card/card_search.pug', title="Search Result", card_data=result)
    elif request.method == "GET":
        return render_template('card/card_list.pug', title="All Cards", card_data=card_list())


@api.route("/card/<card_id>")
@page_error_handling
def card(card_id):
    return render_template('card/card_detail.pug', title="Card Details", card_data=card_detail(card_id), owner_detail=user_detail(card_detail(card_id)["data"]["card"]["userID"]))


@api.route("/create-card", methods=["Get", "POST"])
@page_error_handling
def create_card():
    if request.method == "POST":
        data = request.form
        card_create(data["UID"])
        return redirect(url_for('cards'))
    elif request.method == "GET":
        return render_template('card/card_create.pug', title="Register new Card")


@api.route("/delete-card/<card_id>", methods=["Get", "Post"])
@page_error_handling
def delete_card(card_id):
    if request.method == "POST":
        data = request.form
        if data["confirmation"] == "1":
            card_delete(card_id)
        return redirect(url_for('cards'))
    elif request.method == "GET":
        return render_template('utils/confirm.pug', title="Delete Card")


@api.route("/update-card/<card_id>", methods=["Get", "Post"])
@page_error_handling
def update_card(card_id):
    if request.method == "POST":
        data = request.form
        card_update(card_id, data["new_id"], None)
        return redirect(url_for('card', card_id=data["new_id"]))
    elif request.method == "GET":
        return render_template('card/card_update.pug', title="Update Card", card_id=card_id)

# Ownership


@api.route("/grant-ownership", methods=["GET", "POST"])
@page_error_handling
def grant_ownership():
    if request.method == "POST":
        data = request.form
        card_update(data["card_UID"], data["card_UID"], data["user_ID"])
        return redirect(url_for('user', user_id=data["user_ID"]))
    elif request.method == "GET":
        return render_template('card/grant_ownership.pug', title="Grant Ownership", user_data=user_list(), card_data=card_list(True))


@api.route("/remove-ownership/<card_id>", methods=["GET", "POST"])
@page_error_handling
def remove_ownership(card_id):
    if request.method == "POST":
        data = request.form
        if data["confirmation"] == "1":
            card_update(card_id, card_id, None)
        return redirect(url_for('card', card_id=card_id))
    elif request.method == "GET":
        return render_template('utils/confirm.pug', title="Remove Ownership")

# Postion pages


@api.route("/postions", methods=['GET', 'POST'])
@page_error_handling
def postions():
    if request.method == "POST":
        data = request.form
        result = []
        for postion in position_list()["data"]["positions"]:
            if data["search"] in postion["name"]:
                result.append(postion)
        return render_template('position/position_search.pug', title="Search Result", postion_data=result)
    elif request.method == "GET":
        return render_template('position/position_list.pug', title="All Postions", postion_data=position_list())


@api.route("/postion/<id>")
@page_error_handling
def postion(id):
    return render_template('position/position_detail.pug', title="All Postions", postion_data=position_detail(id))


@api.route("/create-postion", methods=["Get", "POST"])
@page_error_handling
def create_postion():
    if request.method == "POST":
        data = request.form
        position_create(data["name"])
        return redirect(url_for('postions'))
    elif request.method == "GET":
        return render_template('position/position_create.pug', title="Create new Postion")


@api.route("/update-postion/<id>", methods=["Get", "POST"])
@page_error_handling
def update_postion(id):
    if request.method == "POST":
        data = request.form
        position_update(id, data["name"])
        return redirect(url_for('postion', id=id))
    elif request.method == "GET":
        return render_template('position/position_update.pug', title="Update Postion", postion_data=position_detail(id))


@api.route("/delete-postion/<id>", methods=["Get", "POST"])
@page_error_handling
def delete_postion(id):
    if request.method == "POST":
        position_delete(id)
        return redirect(url_for('postions'))
    elif request.method == "GET":
        position_user = [] 
        for user in user_list()["data"]["users"]: 
            if user["position_id"] == int(id):
                position_user.append(user)
        return render_template('position/position_delete.pug', title="Delete Postion", len=len(position_user), user_data=position_user)

# IOT Paths


@api.route("/log", methods=["POST"])
def log():
    if request.method == "POST":
        try:
            data = request.get_json()
            if check_key(data["key"]) is False:
                return {"error": "Incorrect API Key"}, 401
            userID = card_detail(data["data"]["UID"])["data"]["card"]["userID"]
            status_update(userID)
            log_create(userID, data["data"]["UID"], int(time.time()), status_detail(userID)["data"]["status"]["status"])
            return jsonify(data), 201
        except Exception as e:
            return {
                "error": str(e)
            }, 400
