from concurrent import futures

import grpc
import weather_commands_pb2
import weather_commands_pb2_grpc


class Weather(weather_commands_pb2_grpc.WeatherServicer):
    def GetWeather(self, request, context):
        response_data = request.city
        response = weather_commands_pb2.WeatherResponse(weather=response_data)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_commands_pb2_grpc.add_WeatherServicer_to_server(Weather(), server)
    server.add_insecure_port("[::]:50001")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
