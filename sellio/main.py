from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sellio.api import router as api_router
from sellio.graph.endpoint import router as graph_router
from sellio.services.db import init_db
from sellio.services.db import main_db
from sellio.services.hash import init_hasher
from sellio.settings import config
from sellio.settings import init_config


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    init_config()
    init_db(config)
    init_hasher()
    yield
    if main_db._engine is not None:
        await main_db.close()


def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )
    app.include_router(graph_router)
    app.include_router(api_router)
    return app


app = make_app()
