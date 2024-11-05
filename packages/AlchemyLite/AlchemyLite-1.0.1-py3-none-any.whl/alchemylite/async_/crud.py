"""
CRUD Operations for async session
"""

from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.inspection import inspect


class AsyncCrudOperation:
    """
    Class, which implements CRUD operations for async session
    """

    def __init__(self, async_session_factory: async_sessionmaker, model, base):
        self.async_session_factory = async_session_factory
        self.model = model
        self.base = base  # Base class of model

    def __validate_params(self, params: dict[str, Any]) -> bool:
        """
        Validate parameters for CRUD operation
        :param params: A dictionary with parameters for CRUD operation
        :return: True, if parameters are valid, else ValueError
        """
        model_columns = {column.name: column.type for column in inspect(self.model).columns}
        for key, value in params.items():
            if key not in model_columns:
                raise ValueError(f'Parameter {key} is not a valid column name')
        return True

    async def create(self, **kwargs) -> None:
        """
        Create operation
        :param params: A dict with parameters and values
        :return: None
        """
        self.__validate_params(kwargs)
        async with self.async_session_factory() as session:
            model = self.model(**kwargs)
            session.add(model)
            await session.commit()

    async def read_all(self) -> list[dict]:
        """
        Read operation
        :return: List[dict]
        """
        async with self.async_session_factory() as session:
            query = select(self.model)
            result = await session.execute(query)
            result = result.scalars().all()
            return [{column: getattr(row, column) for column in row.__table__.columns.keys()} for
                    row in result]

    async def limited_read(self, limit: int = 50, offset: int = 0) -> list[dict]:
        """
        Read operation with limit and offset
        :param limit: limit
        :param offset: offset
        :return: list[dict]
        """
        async with self.async_session_factory() as session:
            query = select(self.model).limit(limit).offset(offset)
            result = await session.execute(query)
            result = result.scalars().all()
            return [{column: getattr(row, column) for column in row.__table__.columns.keys()} for
                    row in result]

    async def read_by_id(self, id: int) -> list[dict]:
        async with self.async_session_factory() as session:
            query = select(self.model).where(self.model.id == id)
            result = await session.execute(query)
            result = result.scalars().all()
            return [{column: getattr(row, column) for column in row.__table__.columns.keys()} for
                    row in result]

    async def update_by_id(self, **kwargs) -> None:
        """
        Update operation
        :param condition: A dict with condition
        :param params: Params for update
        :return: None
        """
        self.__validate_params(kwargs)
        if 'id' not in kwargs:
            raise ValueError(f'Parameter "id" is missing')
        id = kwargs['id']
        if type(id) is not int:
            raise ValueError(f'Parameter "id" must be an integer')

        async with self.async_session_factory() as session:
            stmt = update(self.model).where(self.model.id == id).values(kwargs)
            await session.execute(stmt)
            await session.commit()

    async def delete_by_id(self, **kwargs) -> None:
        """
        Delete operation
        :param condition: A dict with condition
        :return: None
        """
        if 'id' not in kwargs:
            raise ValueError(f'Parameter "id" is missing')
        id = kwargs['id']
        if type(id) is not int:
            raise ValueError(f'Parameter "id" must be an integer')

        async with self.async_session_factory() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()

    async def create_all_tables(self) -> None:
        async with self.async_session_factory() as session:
            self.base.metadata.create_all(bind=session.get_bind())

    async def delete_all_tables(self) -> None:
        async with self.async_session_factory() as session:
            self.base.metadata.drop_all(bind=session.get_bind())
