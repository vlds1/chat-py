import asyncio

import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("Connected to server")


@sio.event
async def disconnect():
    print("Disconnected from server")


@sio.event
async def message(data):
    print("Received message:", data)


async def send_message():
    recipient_id = input("recipient_id:")
    user_id = input("user_id:")
    await sio.emit(
        "join_room",
        data={"user_id": user_id, "recipient_id": recipient_id},
        namespace="/",
    )

    while True:
        msg = input("Enter message: ")
        await sio.emit(
            "message",
            data={
                "user_id": user_id,
                "recipient_id": recipient_id,
                "message": msg
            },
            namespace="/",
        )
        await asyncio.sleep(0.1)


async def main():
    await sio.connect("http://localhost:8080", namespaces=["/"])
    await send_message()


asyncio.run(main())
