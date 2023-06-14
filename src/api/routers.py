from fastapi.routing import APIRouter
from starlette.routing import Mount

from src.api.weather.consumer import routers as consumer_router
from src.api.weather.endpoints import routers as record_router
from src.api.weather.graphql import graphql_app
#  -> How to add a new route example:
#  -> from src.api.deposit.endpoints import routers as routers_deposit

routers = APIRouter()

#  -> routers.include_router(routers_deposit, tags=["Deposit"])
routers.include_router(record_router)
routers.include_router(consumer_router)


graphql_routes = [
    Mount("/graphql/", graphql_app),
]
