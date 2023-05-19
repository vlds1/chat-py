import socketio
import uvicorn
from namespaces.namespaces import DefaultNameSpace
from core.config import app_config


sio = socketio.AsyncServer(async_mode="asgi", logger=True)
sio.register_namespace(DefaultNameSpace("/"))
app = socketio.ASGIApp(sio)


if __name__ == "__main__":
    uvicorn.run(app, host=app_config.host, port=app_config.port)
