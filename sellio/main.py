from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from typing_extensions import TypedDict

from sellio.api import router as api_router
from sellio.graph.endpoint import router as graph_router
from sellio.services.db import sessionmanager
from sellio.settings import Config


class AppState(TypedDict):
    config: Config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppState, None]:
    state = AppState(
        config=app.state.config,
    )
    yield state
    if sessionmanager._engine is not None:
        await sessionmanager.close()


def make_app() -> FastAPI:
    config = Config.load()
    app = FastAPI(
        lifespan=lifespan,
    )
    app.state.config = config
    app.include_router(graph_router)
    app.include_router(api_router)
    return app


app = make_app()
