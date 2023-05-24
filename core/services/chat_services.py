import aio_pika
from config import get_config
from logger.logger_config import console_log


class RabbitService:
    def __init__(self):
        self.config = get_config()
        self.logger = console_log

    async def get_rabbit(self):
        connection = await aio_pika.connect_robust(
            login=self.config.RABBIT_LOGIN,
            password=self.config.RABBIT_PASSWORD,
            host=self.config.RABBIT_HOST,
        )
        channel = await connection.channel()
        return channel

    async def send_message(self, message, from_user, to_user):
        rabbit_channel = await self.get_rabbit()
        await rabbit_channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                headers={"from_user": from_user, "to_user": to_user},
            ),
            routing_key="chat-queue",
        )
        self.logger.info("[rabbit_producer] message sent")
