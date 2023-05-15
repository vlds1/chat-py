def get_room_id(data: dict) -> str:
    user_id = data["user_id"]
    recipient_id = data["recipient_id"]
    if user_id > recipient_id:
        room_id = f"{user_id}-{recipient_id}"
    else:
        room_id = f"{recipient_id}-{user_id}"

    return room_id
