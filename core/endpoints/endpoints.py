from flask import Blueprint, jsonify

auth = Blueprint(
    "test",
    __name__,
)


@auth.route("/", methods=["GET", "POST"])
async def test():
    return jsonify({"test"})
