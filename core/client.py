import asyncio

from services.rabbit_services import RabbitService

rabbit = RabbitService()


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(rabbit.consume_commands())
    loop.run_until_complete(rabbit.consume_commands())


if __name__ == "__main__":
    asyncio.run(main())
