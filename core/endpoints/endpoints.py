from endpoints.crud import AuthUser, Token
from flask import Blueprint, make_response, request

auth = Blueprint(
    "authentication",
    __name__,
)


@auth.route("/registration", methods=["POST"])
async def registration():
    user = AuthUser()
    registration_res = await user.create_new_user(request.get_json())
    return make_response(registration_res)


@auth.route("/login", methods=["POST"])
async def login():
    user = AuthUser()
    login_res = await user.login_user(request.get_json())
    return make_response(login_res)


@auth.route("/token/refresh", methods=["POST"])
async def refresh_access_token():
    token = Token()
    new_access_token = await token.update_access_token(request.get_json())
    return make_response(new_access_token)
