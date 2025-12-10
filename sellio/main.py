from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sellio.api import router as api_router
from sellio.graph.endpoint import router as graph_router
from sellio.middleware.request_context import RequestContextMiddleware
from sellio.services.categories import init_cached_categories
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
    await init_cached_categories()

    yield
    if main_db._engine is not None:
        await main_db.close()


def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Add request context middleware for global access to request/response
    app.add_middleware(RequestContextMiddleware)

    app.include_router(graph_router)
    app.include_router(api_router)
    return app


app = make_app()
