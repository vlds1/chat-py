import uuid

import socketio

from core.config import get_config
from core.logger.logger_config import get_logger
from core.schemas.schemas import MessageSchema
from core.services.chat_services import RabbitService, auth_required


class DefaultNameSpace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.room_id = uuid.uuid4()
        self.rabbit = RabbitService()
        self.logger = get_logger()
        self.config = get_config()
        super().__init__(*args, **kwargs)

    @auth_required
    async def on_connect(self, sid: str, environ: dict) -> None:
        self.enter_room(sid, self.room_id)
        self.logger.info(f"{sid} connected to room: {self.room_id}")

    async def on_disconnect(self, sid: str) -> None:
        self.leave_room(sid, self.room_id)
        self.logger.info(f"{sid} disconnected from room: {self.room_id}")

    @auth_required
    async def on_message(self, sid: str, data: dict) -> None:
        try:
            message_data = MessageSchema(**data)
            message = message_data.message
            from_user = message_data.from_user
            to_user = message_data.to_user
            match message.startswith("/"):
                case True:
                    await self.rabbit.send_message(
                        message=message,
                        from_user=from_user,
                        to_user=to_user,
                        routing_key=self.config.COMMAND_ROUTING_KEY,
                        sender_sid=sid,
                    )
                    async for message in self.rabbit.consume():
                        self.logger.info("[rabbit_consumer_ws] message received")
                        await self.emit(
                            "message",
                            message.body.decode("utf-8"),
                            room=message.headers["sender_sid"],
                        )
                case False:
                    await self.emit("message", message, room=self.room_id, skip_sid=sid)
                    await self.rabbit.send_message(
                        message=message,
                        from_user=from_user,
                        to_user=to_user,
                        routing_key=self.config.CHAT_ROUTING_KEY,
                        sender_sid=sid,
                    )
        except Exception as e:
            self.logger.error(f"[on_message] {e}")
