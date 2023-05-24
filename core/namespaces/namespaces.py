import uuid

import socketio
from services.chat_services import RabbitService


class DefaultNameSpace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.room_id = uuid.uuid4()
        self.rabbit = RabbitService()
        super().__init__(*args, **kwargs)

    async def on_connect(self, sid: str, environ: dict) -> None:
        self.enter_room(sid, self.room_id)
        print(f"{sid} connected to room: {self.room_id}")

    async def on_disconnect(self, sid: str) -> None:
        self.leave_room(sid, self.room_id)
        print(f"{sid} disconnected from room: {self.room_id}")

    async def on_message(self, sid: str, data: dict) -> None:
        try:
            message = data["message"]
            from_user = data["from_user"]
            to_user = data["to_user"]

            await self.emit("message", message, room=self.room_id, skip_sid=sid)
            await self.rabbit.send_message(message, from_user, to_user)
            print("[on_message] message sent")
        except Exception as e:
            print("on message", e)
