import asyncio
import sys
from pathlib import Path

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from src.api import routers
from src.api.routers import graphql_routes
from src.api.weather.consumer import Consumer
from src.core import get_settings
from src.core.redis_tools.tools import redis_cache
from src.core.settings.mongodb import get_mongo_client
from src.core.settings.mongodb import weather_data_collection

sys.path.append(str(Path(__file__).parent.parent))


settings = get_settings()
db_client = get_mongo_client()
consumer = Consumer(collection=weather_data_collection)


def get_application() -> "FastAPI":
    """Get FastAPI app"""

    app = FastAPI(
        title=settings.project_name,
        root_path=settings.root_path,
        version=settings.app_version,
        debug=True,
        routes=graphql_routes,
        dependencies=[
            Depends(RateLimiter(times=5, seconds=10)),
        ],
    )

    app.include_router(routers, prefix=settings.api_prefix)
    return app


app = get_application()


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
    app.state.db_client = db_client

    await FastAPILimiter.init(redis_cache)
    asyncio.create_task(consumer.consume())


def main():
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == "__main__":
    main()
