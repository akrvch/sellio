from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from typing_extensions import TypedDict

from sellio.graph.endpoint import router
from sellio.settings import Config


class AppState(TypedDict):
    config: Config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppState, None]:
    state = AppState(
        config=app.state.config,
    )
    yield state


def make_app() -> FastAPI:
    config = Config.load()
    app = FastAPI(
        lifespan=lifespan,
    )
    app.state.config = config
    app.include_router(router, tags=["GraphQL"])
    return app


app = make_app()
