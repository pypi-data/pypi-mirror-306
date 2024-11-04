from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager, suppress
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any

import anyio.lowlevel
import sqlalchemy as sa

from typed_diskcache import exception as te
from typed_diskcache.core.context import aconn_context, conn_context
from typed_diskcache.core.types import EvictionPolicy
from typed_diskcache.database import connect as db_connect
from typed_diskcache.database.model import Cache

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Callable, Generator, Mapping
    from os import PathLike

    from sqlalchemy.engine import Connection as SAConnection
    from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

    from typed_diskcache.model import Settings


__all__ = ["Connection"]


class Connection:
    """Database connection."""

    def __init__(
        self,
        database: str | PathLike[str],
        timeout: float,
        sync_scopefunc: Callable[[], Any] | None = None,
        async_scopefunc: Callable[[], Any] | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._database = Path(database)
        self._timeout = timeout

        self._sync_scopefunc = sync_scopefunc
        self._async_scopefunc = async_scopefunc
        self._settings = settings

    def __getstate__(self) -> Mapping[str, Any]:
        import cloudpickle

        sync_scope = (
            None
            if self._sync_scopefunc is None
            else cloudpickle.dumps(self._sync_scopefunc)
        )
        async_scope = (
            None
            if self._async_scopefunc is None
            else cloudpickle.dumps(self._async_scopefunc)
        )

        return {
            "database": str(self._database),
            "timeout": self._timeout,
            "sync_scopefunc": sync_scope,
            "async_scopefunc": async_scope,
            "settings": None
            if self._settings is None
            else self._settings.model_dump_json(),
        }

    def __setstate__(self, state: Mapping[str, Any]) -> None:
        import cloudpickle

        from typed_diskcache.model import Settings

        self._database = Path(state["database"])
        self.timeout = state["timeout"]
        self._sync_scopefunc = (
            None
            if state["sync_scopefunc"] is None
            else cloudpickle.loads(state["sync_scopefunc"])
        )
        self._async_scopefunc = (
            None
            if state["async_scopefunc"] is None
            else cloudpickle.loads(state["async_scopefunc"])
        )
        self._settings = (
            None
            if state["settings"] is None
            else Settings.model_validate_json(state["settings"])
        )

    @property
    def timeout(self) -> float:
        """Return the timeout."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        """Set the timeout."""
        self._timeout = value

    @cached_property
    def _sync_url(self) -> sa.URL:
        return db_connect.create_sqlite_url(self._database, is_async=False)

    @cached_property
    def _async_url(self) -> sa.URL:
        return db_connect.create_sqlite_url(self._database, is_async=True)

    @cached_property
    def _sync_engine(self) -> sa.Engine:
        engine = db_connect.ensure_sqlite_sync_engine(self._sync_url)
        if self._settings is None:
            return engine

        return db_connect.set_listeners(engine, self._settings.sqlite_settings)

    @cached_property
    def _async_engine(self) -> AsyncEngine:
        engine = db_connect.ensure_sqlite_async_engine(self._async_url)
        if self._settings is None:
            return engine

        return db_connect.set_listeners(engine, self._settings.sqlite_settings)

    @contextmanager
    def connect(self) -> Generator[SAConnection, None, None]:
        """Connect to the database."""
        conn = conn_context.get()
        if conn is not None:
            yield conn
            return

        with self._sync_engine.connect() as connection:
            yield connection

    @asynccontextmanager
    async def aconnect(self) -> AsyncGenerator[AsyncConnection, None]:
        """Connect to the database."""
        conn = aconn_context.get()
        if conn is not None:
            await anyio.lowlevel.checkpoint()
            yield conn
            return

        async with self._async_engine.connect() as connection:
            yield connection

    def close(self) -> None:
        """Close the connection."""
        if "_sync_engine" in self.__dict__:
            self._sync_engine.dispose(close=True)
        if "_async_engine" in self.__dict__:
            self._async_engine.sync_engine.dispose(close=True)
        for key in (
            "_sync_engine",
            "_async_engine",
            "_sync_registry",
            "_async_registry",
        ):
            self.__dict__.pop(key, None)

    async def aclose(self) -> None:
        """Close the connection."""
        if "_sync_engine" in self.__dict__:
            self._sync_engine.dispose(close=True)
        if "_async_engine" in self.__dict__:
            await self._async_engine.dispose(close=True)
        for key in (
            "_sync_engine",
            "_async_engine",
            "_sync_registry",
            "_async_registry",
        ):
            self.__dict__.pop(key, None)

    def update_settings(self, settings: Settings) -> None:
        """Update the settings."""
        self.close()
        self._settings = settings

    @property
    def eviction(self) -> Eviction:
        """Return the eviction policy manager."""
        return Eviction(self)

    def __del__(self) -> None:
        with suppress(BaseException):
            self.close()


class Eviction:
    def __init__(self, conn: Connection) -> None:
        if conn._settings is None:  # noqa: SLF001
            raise te.TypedDiskcacheValueError("settings is not set")

        self._conn = conn
        self._policy = conn._settings.eviction_policy  # noqa: SLF001

    @property
    def get(self) -> sa.Update | None:
        if self._policy == EvictionPolicy.LEAST_RECENTLY_USED:
            return (
                sa.update(Cache)
                .values(access_time=sa.bindparam("access_time", type_=sa.Float()))
                .where(Cache.id == sa.bindparam("id", type_=sa.Integer()))
            )
        if self._policy == EvictionPolicy.LEAST_FREQUENTLY_USED:
            return (
                sa.update(Cache)
                .values(access_count=sa.bindparam("access_count", type_=sa.Integer()))
                .where(Cache.id == sa.bindparam("id", type_=sa.Integer()))
            )
        return None

    @property
    def cull(self) -> sa.Select[tuple[Cache]] | None:
        if self._policy == EvictionPolicy.LEAST_RECENTLY_STORED:
            return (
                sa.select(Cache)
                .order_by(Cache.store_time)
                .limit(sa.bindparam("limit", type_=sa.Integer()))
            )
        if self._policy == EvictionPolicy.LEAST_RECENTLY_USED:
            return (
                sa.select(Cache)
                .order_by(Cache.access_time)
                .limit(sa.bindparam("limit", type_=sa.Integer()))
            )
        if self._policy == EvictionPolicy.LEAST_FREQUENTLY_USED:
            return (
                sa.select(Cache)
                .order_by(Cache.access_count)
                .limit(sa.bindparam("limit", type_=sa.Integer()))
            )
        return None
