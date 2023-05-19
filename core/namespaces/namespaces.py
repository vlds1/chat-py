import uuid

import socketio

from core.services.chat_services import get_room_id


class DefaultNameSpace(socketio.AsyncNamespace):
    async def on_connect(self, sid: str, environ: dict) -> None:
        print(f"connected, id: {sid}")

    async def on_disconnect(self, sid: str) -> None:
        print(f"disconnected {sid}")

    async def on_join_room(self, sid: str, data: dict) -> None:
        try:
            room_id = uuid.uuid4()
            self.enter_room(sid, room_id)
        except Exception as e:
            print(e)

    async def on_message(self, sid: str, data: dict) -> None:
        try:
            message = data["message"]
            room_id = get_room_id(data)
            await self.emit("message", message, room=room_id, skip_sid=sid)
        except Exception as e:
            print(e)
