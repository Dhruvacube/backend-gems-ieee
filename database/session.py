import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .vars import envConfig

log = logging.getLogger(__name__)


class Session:
    """
    This class is used to create a session with the database.
    """

    @staticmethod
    def get_engine() -> AsyncEngine:
        """
        This function is used to get the engine for the database.
        """
        return create_async_engine(envConfig.DATABASE_URL, echo=False)

    @staticmethod
    def get_session() -> sessionmaker:
        """Return the database session connection."""
        db_session = sessionmaker(
            bind=Session.get_engine(),  # type: ignore
            autoflush=True,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        return db_session



session_obj: Any = Session.get_session()
