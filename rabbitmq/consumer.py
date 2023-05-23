import asyncio

from aio_pika import connect_robust
from consumer_service import EmailService


async def consume():
    email = EmailService()
    connection = await connect_robust(login="user", password="password", host="rabbit")
    channel = await connection.channel()

    queue = await channel.declare_queue("chat-queue", durable=True)
    print("[consumer] connected to rabbit")
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                await email.send_mail(message=message)


loop = asyncio.get_event_loop()
loop.create_task(consume())
loop.run_until_complete(consume())
