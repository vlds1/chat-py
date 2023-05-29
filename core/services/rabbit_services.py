import aio_pika
from aio_pika import connect_robust
from config.config import get_config
from logger.log import get_logger
from services.grpc_services import CommandService


class RabbitService:
    def __init__(self):
        self.config = get_config()
        self.command_service = CommandService()
        self.logger = get_logger()

    async def get_rabbit(self):
        connection = await connect_robust(
            login=self.config.RABBIT_LOGIN,
            password=self.config.RABBIT_PASSWORD,
            host=self.config.RABBIT_HOST,
        )
        return connection

    async def consume_commands(self):
        connection = await self.get_rabbit()
        channel = await connection.channel()
        commands_queue = await channel.declare_queue("command-queue", durable=True)
        async with commands_queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    sender_sid = message.headers["sender_sid"]
                    weather_res = self.command_service.send_req(
                        command=message.body.decode("utf-8")
                    )
                    self.logger.info(
                        f"[rabbit consumer] get res from grpc: {weather_res.weather}"
                    )
                    await self.send_command_res_message(
                        data=weather_res.weather, sender_sid=sender_sid
                    )

    async def send_command_res_message(self, data, sender_sid):
        connection = await self.get_rabbit()
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=f"{data}".encode(), headers={"sender_sid": sender_sid}
            ),
            routing_key="command_res-queue",
        )
