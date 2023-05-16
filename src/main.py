import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter

from src.api import routers
from src.api.routers import graphql_routes
from src.core import get_settings
from src.core.redis_tools.tools import redis_client
from src.core.settings.mongodb import get_mongo_client

sys.path.append(str(Path(__file__).parent.parent))


settings = get_settings()
db_client = get_mongo_client()


def get_application() -> "FastAPI":
    """Get FastAPI app"""

    app = FastAPI(
        title=settings.project_name,
        root_path=settings.root_path,
        version=settings.app_version,
        debug=True,
        routes=graphql_routes,
    )

    app.include_router(routers, prefix=settings.api_prefix)
    return app


app = get_application()


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    app.state.db_client = db_client

    await FastAPILimiter.init(redis_client)


def main():
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == "__main__":
    main()
