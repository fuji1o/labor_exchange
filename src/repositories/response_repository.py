from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Job as JobModel
from models import Response as ResponseModel
from models import User as UserModel
from storage.sqlalchemy.tables import Response
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
        return self.__to_response_model(response_from_db=response, include_relations=False)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(Response.user), selectinload(Response.job))

            res = await session.execute(query)
            response_from_db = res.scalars().first()

        response_model = self.__to_response_model(
            response_from_db=response_from_db, include_relations=include_relations
        )
        return response_model

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

        response_models = []
        for response in responses_from_db:
            model = self.__to_response_model(
                response_from_db=response, include_relations=include_relations
            )
            response_models.append(model)

        return response_models

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

        return self.__to_response_model(response_from_db, include_relations=False)

    async def delete(self, id: int):
        async with self.session() as session:
            query = delete(Response).where(Response.id == id)
            res = await session.execute(query)
            await session.commit()

            if res.rowcount == 0:
                raise ValueError("Отклик не найден")

        return None

    @staticmethod
    def __to_response_model(
        response_from_db: Response, include_relations: bool = False
    ) -> ResponseModel:
        user_model = None
        job_model = None

        if response_from_db:
            if include_relations:
                if response_from_db.user:
                    user_model = UserModel(
                        id=response_from_db.user.id,
                        name=response_from_db.user.name,
                        email=response_from_db.user.email,
                        is_company=response_from_db.user.user.is_company,
                    )
                if response_from_db.user.job:
                    job_model = JobModel(
                        id=response_from_db.job.id,
                        user_id=response_from_db.job.user_id,
                        title=response_from_db.job.title,
                        description=response_from_db.job.description,
                        salary_from=response_from_db.job.salary_from,
                        salary_to=response_from_db.job.salary_to,
                        is_active=response_from_db.job.is_active,
                        created_at=response_from_db.job.created_at,
                    )

            response_model = ResponseModel(
                id=response_from_db.id,
                job_id=response_from_db.job_id,
                user_id=response_from_db.user_id,
                message=response_from_db.message,
                user=user_model,
                job=job_model,
            )
            return response_model

        return None
