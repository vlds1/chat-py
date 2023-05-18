from flask import Blueprint, make_response, request

from core.endpoints.crud import create_new_user, login_user, update_access_token

auth = Blueprint(
    "authentication",
    __name__,
)


@auth.route("/registration", methods=["POST"])
async def registration():
    registration_res = await create_new_user(request.get_json())
    return make_response(registration_res)


@auth.route("/login", methods=["POST"])
async def login():
    login_res = await login_user(request.get_json())
    return make_response(login_res)


@auth.route("/token/refresh", methods=["POST"])
async def refresh_access_token():
    new_access_token = await update_access_token(request.get_json())
    return make_response(new_access_token)
