import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
from typing import cast

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from sellio import GlobalProxy
from sellio import global_storage
from sellio.settings import Config

log = logging.getLogger(__name__)


class DatabaseSessionManager:
    def __init__(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


_KEY = "main_db.session_manager"
main_db: DatabaseSessionManager = cast(
    DatabaseSessionManager, GlobalProxy(_KEY)
)


def init_db(config: Config):
    global_storage.set(_KEY, DatabaseSessionManager(host=config.main_db.url))
    log.info("Main DB engine successfully configured")
