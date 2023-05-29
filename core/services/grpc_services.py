import grpc
import weather_commands_pb2
import weather_commands_pb2_grpc
from config.config import get_config
from logger.log import logger


class CommandService:
    def __init__(self):
        self.logger = logger
        self.config = get_config()

    def send_req(self, command):
        with grpc.insecure_channel(f"{self.config.GRPC_HOST}:50051") as channel:
            city = command.split()[1]
            stub = weather_commands_pb2_grpc.WeatherStub(channel)
            request = weather_commands_pb2.WeatherRequest(city=city)
            response = stub.GetWeather(request)
            return response
