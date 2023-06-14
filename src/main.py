import asyncio
import aioredis
import sys
from pathlib import Path
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from motor.motor_asyncio import AsyncIOMotorClient
from src.api.weather.consumer import Consumer

from src.api.routers import routers, graphql_routes
from src.core.settings.settings import Settings
from src.dependencies import get_settings

sys.path.append(str(Path(__file__).parent.parent))



def get_application(settings: Settings) -> "FastAPI":
    """Get FastAPI app"""

    app = FastAPI(
        title=settings.project_name,
        root_path=settings.root_path,
        version=settings.app_version,
        routes=graphql_routes,
        # dependencies=[
        #     Depends(RateLimiter(times=5, seconds=10)),
        # ],
    )

    app.include_router(routers, prefix=settings.api_prefix)
    return app

settings = Settings()
app = get_application(settings=settings)

def main(settings: Settings = Depends(get_settings)):
    uvicorn.run(**settings.uvicorn.dict())
    

@app.on_event("startup")
async def startup_event():
        redis = aioredis.from_url(
            settings.redis_cache_url, encoding="utf-8", decode_responses=True
        )
        collection = AsyncIOMotorClient(settings.mongodb_url).weather_app.get_collection("weather_data")
        consumer = Consumer(collection, settings=settings)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        await FastAPILimiter.init(redis)

    


if __name__ == "__main__":
    main()
