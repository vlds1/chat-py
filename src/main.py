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
from src.api.routers import routers
from src.core.settings.settings import Settings
from src.dependencies import get_settings
from src.api.weather.graphql_utils import graphql_app

sys.path.append(str(Path(__file__).parent.parent))


def get_application(settings: Settings, init_extras: bool = True) -> "FastAPI":
    """Get FastAPI app"""

    dependencies = []
    if init_extras:
        dependencies.append(Depends(RateLimiter(times=5, seconds=10)))

    app = FastAPI(
        title=settings.project_name,
        # routes=graphql_routes,
    )

    app.include_router(routers, prefix=settings.api_prefix)
    app.mount("/graphql", graphql_app)

    if init_extras:

        @app.on_event("startup")
        async def startup_event():
            redis = aioredis.from_url(
                settings.redis_cache_url,
                encoding="utf-8",
                decode_responses=True,
            )
            collection = AsyncIOMotorClient(
                settings.mongodb_url
            ).weather_app.get_collection("weather_data")
            consumer = Consumer(collection, settings=settings)
            asyncio.create_task(consumer.consume())
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
            asyncio.create_task(FastAPILimiter.init(redis))

    return app


settings = Settings()  # type: ignore
app = get_application(settings=settings)


def main(settings: Settings = Depends(get_settings)):
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == "__main__":
    main()
