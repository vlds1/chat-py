import socketio
import uvicorn
from config import AppConfig
from namespaces.namespaces import DefaultNameSpace

sio = socketio.AsyncServer(async_mode="asgi", logger=True)
sio.register_namespace(DefaultNameSpace("/"))
app = socketio.ASGIApp(sio)


if __name__ == "__main__":
    app_config = AppConfig()
    uvicorn.run(app, host=app_config.host, port=int(app_config.port))
