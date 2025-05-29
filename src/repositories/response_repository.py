from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Response as ResponseModel
from storage.sqlalchemy.tables import Response
from tools.converter import to_model
from tools.updater import update_model
from web.schemas.response import ResponseCreateSchema, ResponseUpdateSchema


class ResponseRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, response_create_dto: ResponseCreateSchema) -> ResponseModel:
        async with self.session() as session:
            response = Response(
                job_id=response_create_dto.job_id,
                user_id=response_create_dto.user_id,
                message=response_create_dto.message,
            )

            session.add(response)
            await session.commit()
            await session.refresh(response)
        return to_model(response, ResponseModel)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(Response.user), selectinload(Response.job))

            res = await session.execute(query)
            response_from_db = res.scalars().first()

        return to_model(response_from_db, ResponseModel) if response_from_db else None

    async def retrieve_many(
        self, limit: int = 100, skip: int = 0, include_relations: bool = False
    ) -> list[ResponseModel]:
        async with self.session() as session:
            query = select(Response).limit(limit).offset(skip)
            if include_relations:
                query = query.options(selectinload(Response.user)).options(
                    selectinload(Response.job)
                )

            res = await session.execute(query)
            responses_from_db = res.scalars().all()

        responses_model = []
        for response in responses_from_db:
            model = to_model(response, ResponseModel)
            responses_model.append(model)

        return responses_model

    async def update(self, id: int, response_update_dto: ResponseUpdateSchema) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()
            if not response_from_db:
                raise ValueError("Отклик не найден")

            update_data = response_update_dto.model_dump(exclude_unset=True)
            update_model(response_from_db, update_data)

            session.add(response_from_db)
            await session.commit()
            await session.refresh(response_from_db)

        return to_model(response_from_db, ResponseModel)

    async def delete(self, id: int):
        async with self.session() as session:
            query = delete(Response).where(Response.id == id)
            res = await session.execute(query)
            await session.commit()

            if res.rowcount == 0:
                raise ValueError("Отклик не найден")

        return None