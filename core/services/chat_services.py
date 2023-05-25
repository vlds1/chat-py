import aio_pika
from aio_pika.abc import AbstractRobustConnection
from config import get_config
from logger.logger_config import console_log


class RabbitService:
    def __init__(self):
        self.config = get_config()
        self.logger = console_log

    async def get_rabbit(self) -> AbstractRobustConnection:
        try:
            connection = await aio_pika.connect_robust(
                login=self.config.RABBIT_LOGIN,
                password=self.config.RABBIT_PASSWORD,
                host=self.config.RABBIT_HOST,
            )
            return connection
        except Exception as e:
            self.logger.error(f"[rabbit] get server error: {e}")

    async def send_message(
        self, message: str, from_user: str, to_user: str, routing_key: str
    ) -> None:
        try:
            rabbit_connection = await self.get_rabbit()
            rabbit_channel = await rabbit_connection.channel()
            await rabbit_channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    headers={"from_user": from_user, "to_user": to_user},
                ),
                routing_key=routing_key,
            )
            await rabbit_connection.close()
            self.logger.info(f"[rabbit_producer] message sent to {routing_key}")
        except Exception as e:
            self.logger.error(f"[rabbit] send message error: {e}")
