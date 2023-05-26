import grpc
import weather_commands_pb2
import weather_commands_pb2_grpc
from logger.log import logger


class CommandService:
    def __init__(self):
        self.logger = logger

    def send_req(self, command):
        with grpc.insecure_channel("localhost:50001") as channel:
            city = command.split()[1]
            stub = weather_commands_pb2_grpc.WeatherStub(channel)
            request = weather_commands_pb2.WeatherRequest(city=city)
            response = stub.GetWeather(request)
            self.logger.info(f"[grpc client] response: {response}")
