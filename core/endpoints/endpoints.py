from flask import Blueprint
from flask import jsonify
from flask import request

from core.endpoints.crud import create_new_user
from core.endpoints.crud import login_user
from core.endpoints.crud import update_access_token

auth = Blueprint(
    "authentication",
    __name__,
)


@auth.route("/registration", methods=["POST"])
async def registration():
    registration_res = await create_new_user(request.get_json())
    return jsonify(registration_res)


@auth.route("/login", methods=["POST"])
async def login():
    registration_res = await login_user(request.get_json())
    return jsonify(registration_res)


@auth.route("/token/refresh", methods=["POST"])
async def refresh_access_token():
    new_access_token = await update_access_token(request.get_json())
    return jsonify(new_access_token)
