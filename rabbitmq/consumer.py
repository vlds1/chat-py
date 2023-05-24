import asyncio

from aio_pika import connect_robust
from config import get_config
from consumer_service import EmailService
from logger.logger_config import get_logger

log = get_logger()


async def consume():
    config = get_config()
    email = EmailService()
    connection = await connect_robust(
        login=config.RABBIT_LOGIN,
        password=config.RABBIT_PASSWORD,
        host=config.RABBIT_HOST,
    )
    channel = await connection.channel()

    queue = await channel.declare_queue("chat-queue", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            log.info("[rabbit_consumer] message received")
            async with message.process():
                await email.send_mail(message=message)
                log.info("[rabbit_consumer] message sent to email")


loop = asyncio.get_event_loop()
loop.create_task(consume())
loop.run_until_complete(consume())
