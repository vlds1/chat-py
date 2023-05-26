import asyncio

from aio_pika import connect_robust
from config.config import get_config
from services.grpc_services import CommandService

config = get_config()


async def consume_commands():
    command_service = CommandService()
    connection = await connect_robust(
        login=config.RABBIT_LOGIN,
        password=config.RABBIT_PASSWORD,
        host=config.RABBIT_HOST,
    )

    channel = await connection.channel()
    commands_queue = await channel.declare_queue("command-queue", durable=True)
    async with commands_queue.iterator() as queue_iterator:
        async for message in queue_iterator:
            async with message.process():
                command_service.send_req(command=message.body.decode("utf-8"))


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(consume_commands())
    loop.run_until_complete(consume_commands())


if __name__ == "__main__":
    asyncio.run(main())
