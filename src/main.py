import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from src.core import get_settings
from src.weather_api.endpoints import routers

sys.path.append(str(Path(__file__).parent.parent))


settings = get_settings()


def get_application() -> "FastAPI":
    """Get FastAPI app"""

    app = FastAPI(
        root_path=settings.root_path,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.include_router(routers, prefix=settings.api_prefix)
    return app


app = get_application()


def main():
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == "__main__":
    main()
