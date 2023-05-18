import datetime

import jwt


async def create_token(user_data: dict, token_type: str, exp: int) -> str:
    payload = {
        "_id": str(user_data["_id"]),
        "email": user_data["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
        "type": token_type,
    }
    token = jwt.encode(
        payload=payload,
        key="b37e50cedcd3e3f1ff64f4afc0422084ae694253cf399326868e07a35f4",
        algorithm="HS256",
    )

    return token
