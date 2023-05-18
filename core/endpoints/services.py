import datetime
import os

import jwt


async def create_token(user_data: dict, token_type: str, exp: int) -> str:
    payload = {
        "_id": str(user_data["_id"]),
        "email": user_data["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
        "type": token_type,
    }
    token = jwt.encode(
        payload=payload, key=os.environ.get("JWT_SECRET_KEY"), algorithm="HS256"
    )

    return token
