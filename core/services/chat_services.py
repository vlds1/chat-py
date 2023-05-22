import aio_pika
from config import RabbitConfig


class RabbitService:
    def __init__(self):
        self.rabbit_config = RabbitConfig()

    async def get_rabbit(self):
        connection = await aio_pika.connect_robust(
            login=self.rabbit_config.login, password=self.rabbit_config.password
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
