from fastapi.routing import APIRouter

#  -> How to add a new route example:
#  -> from src.api.deposit.endpoints import routers as routers_deposit
from src.api.weather.endpoints import routers as record_router
from src.api.weather.consumer import routers as consumer_router
from src.core.settings import get_settings

settings = get_settings()
routers = APIRouter()

#  -> routers.include_router(routers_deposit, tags=["Deposit"])
routers.include_router(record_router)
routers.include_router(consumer_router)


