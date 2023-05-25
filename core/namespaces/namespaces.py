import uuid

import socketio
from config import get_config
from logger.logger_config import get_logger
from schemas.schemas import MessageSchema
from services.chat_services import RabbitService


class DefaultNameSpace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.room_id = uuid.uuid4()
        self.rabbit = RabbitService()
        self.logger = get_logger()
        self.config = get_config()
        super().__init__(*args, **kwargs)

    async def on_connect(self, sid: str, environ: dict) -> None:
        self.enter_room(sid, self.room_id)
        self.logger.info(f"{sid} connected to room: {self.room_id}")

    async def on_disconnect(self, sid: str) -> None:
        self.leave_room(sid, self.room_id)
        self.logger.info(f"{sid} disconnected from room: {self.room_id}")

    async def on_message(self, sid: str, data: dict) -> None:
        try:
            message_data = MessageSchema(**data)
            message = message_data.message
            from_user = message_data.from_user
            to_user = message_data.to_user

            match message.startswith("/"):
                case True:
                    await self.rabbit.send_message(
                        message, from_user, to_user, self.config.COMMAND_ROUTING_KEY
                    )
                case False:
                    await self.emit("message", message, room=self.room_id, skip_sid=sid)
                    await self.rabbit.send_message(
                        message, from_user, to_user, self.config.CHAT_ROUTING_KEY
                    )
        except Exception as e:
            self.logger.error(f"[on_message] {e}")
