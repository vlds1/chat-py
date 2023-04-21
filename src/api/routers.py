from fastapi.routing import APIRouter

#  -> How to add a new route example:
#  -> from src.api.deposit.endpoints import routers as routers_deposit
from src.api.weather.consumer import routers as routers_show
from src.core.settings import get_settings

settings = get_settings()
routers = APIRouter()

#  -> routers.include_router(routers_deposit, tags=["Deposit"])
routers.include_router(routers_show)

