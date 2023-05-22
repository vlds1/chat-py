import uuid

import socketio


class DefaultNameSpace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.room_id = uuid.uuid4()
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
            await self.emit("message", message, room=self.room_id, skip_sid=sid)
        except Exception as e:
            print(e)
