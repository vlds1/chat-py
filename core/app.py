import socketio
import uvicorn

from core.config import get_config
from core.namespaces.namespaces import DefaultNameSpace

sio = socketio.AsyncServer(async_mode="asgi", logger=True)
sio.register_namespace(DefaultNameSpace("/"))
app = socketio.ASGIApp(sio)


if __name__ == "__main__":
    app_config = get_config()
    uvicorn.run(app, host=app_config.APP_HOST, port=int(app_config.APP_PORT))
