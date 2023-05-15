import socketio
import uvicorn
from namespaces.namespaces import DefaultNameSpace

sio = socketio.AsyncServer(async_mode="asgi", logger=True)
sio.register_namespace(DefaultNameSpace("/"))
app = socketio.ASGIApp(sio)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
