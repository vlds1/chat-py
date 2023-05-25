import uuid

import socketio
from logger.logger_config import get_logger
from services.chat_services import RabbitService


class DefaultNameSpace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.room_id = uuid.uuid4()
        self.rabbit = RabbitService()
        self.logger = get_logger()
        super().__init__(*args, **kwargs)

    async def on_connect(self, sid: str, environ: dict) -> None:
        self.enter_room(sid, self.room_id)
        self.logger.info(f"{sid} connected to room: {self.room_id}")

    async def on_disconnect(self, sid: str) -> None:
        self.leave_room(sid, self.room_id)
        self.logger.info(f"{sid} disconnected from room: {self.room_id}")

    async def on_message(self, sid: str, data: dict) -> None:
        try:
            message = data["message"]
            from_user = data["from_user"]
            to_user = data["to_user"]

            await self.emit("message", message, room=self.room_id, skip_sid=sid)
            await self.rabbit.send_message(message, from_user, to_user)
        except Exception as e:
            self.logger.error(f"[on_message] {e}")
