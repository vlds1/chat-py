import asyncio

from aio_pika import connect_robust
from config import get_config
from consumer_service import EmailService


async def consume():
    config = get_config()
    email = EmailService()
    print(config.RABBIT_LOGIN, config.RABBIT_PASSWORD, config.RABBIT_HOST)
    connection = await connect_robust(
        login=config.RABBIT_LOGIN,
        password=config.RABBIT_PASSWORD,
        host=config.RABBIT_HOST,
    )
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
