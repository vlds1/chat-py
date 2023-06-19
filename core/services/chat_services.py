import datetime
from functools import wraps

import aio_pika
import jwt
from aio_pika.abc import AbstractRobustConnection

from core.config import get_config
from core.logger.logger_config import console_log


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
        self,
        message: str,
        from_user: str,
        to_user: str,
        routing_key: str,
        sender_sid: str,
    ) -> None:
        try:
            rabbit_connection = await self.get_rabbit()
            rabbit_channel = await rabbit_connection.channel()
            await rabbit_channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    headers={
                        "from_user": from_user,
                        "to_user": to_user,
                        "sender_sid": sender_sid,
                    },
                ),
                routing_key=routing_key,
            )
            await rabbit_connection.close()
            self.logger.info(f"[rabbit_producer] message sent to {routing_key}")
        except Exception as e:
            self.logger.error(f"[rabbit] send message error: {e}")

    async def consume(self):
        connection = await self.get_rabbit()
        channel = await connection.channel()
        queue = await channel.declare_queue("command_res-queue", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                yield message
                await message.ack()


def auth_required(func):
    @wraps(func)
    async def wrapper(*args):
        try:
            self = args[0]
            sid = args[1]
            environ = list(self.server.environ.values())[0]

            access_token = environ.get("HTTP_AUTHENTICATION").split(" ")[1]
            decoded_token = jwt.decode(
                access_token, key=get_config().JWT_SECRET_KEY, algorithms="HS256"
            )
            current_datetime = datetime.datetime.utcnow()
            is_valid = current_datetime < datetime.datetime.fromtimestamp(
                decoded_token["exp"]
            )
            if is_valid:
                return await func(*args)
            else:
                raise Exception
        except Exception:
            await self.disconnect(sid=sid)

    return wrapper
