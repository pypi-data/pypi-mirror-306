"""
Configuration for async session
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from alchemylite import BaseConfig


class AsyncConfig(BaseConfig):
    """
    Class for configuring async sessions
    """
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def session(self):
        async_engine = create_async_engine(
            url=self.DATABASE_URL,
        )
        async_session = async_sessionmaker(
            async_engine,
            expire_on_commit=False,
        )
        return async_session
