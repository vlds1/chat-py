import sys
from pathlib import Path

from src.core.settings.mongodb import mongo_client

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI


from src.api import routers
from src.core import get_settings

from src.migrations import run_migrations


settings = get_settings()


def get_application() -> "FastAPI":
    """Get FastAPI app"""

    app = FastAPI(
        title=settings.project_name,
        root_path=settings.root_path,
        version=settings.app_version,
        debug=settings.debug
    )

    app.include_router(routers, prefix=settings.api_prefix)
    return app


app = get_application()
app.state.mongo_client = mongo_client


def main():
    run_migrations(db_url=str(settings.sqlalchemy.url))
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == "__main__":
    main()
