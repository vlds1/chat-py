import sys
from pathlib import Path


# This path was added to solve some problems with absolute
# imports in order to run this script as an executable file.
from weather_api.endpoints import routers

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
from src.core import get_settings


settings = get_settings()


def get_application() -> "FastAPI":
    """Get FastAPI app"""

    app = FastAPI(
        root_path=settings.root_path,
        version=settings.app_version,
        debug=settings.debug
    )

    app.include_router(routers, prefix=settings.api_prefix)
    return app


app = get_application()

# -> if you need something to do when app starts
# @app.on_event('startup')
# def on_startup():
#     . . .


def main():
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == "__main__":
    main()
