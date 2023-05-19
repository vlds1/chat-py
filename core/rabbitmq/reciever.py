import asyncio

from aio_pika import connect_robust

from core.endpoints.services import EmailService


async def consume():
    email = EmailService()
    connection = await connect_robust(login="user", password="password")
    channel = await connection.channel()

    queue = await channel.declare_queue("chat-queue", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                await email.send_mail(message=message)


loop = asyncio.get_event_loop()
loop.create_task(consume())
loop.run_until_complete(consume())
