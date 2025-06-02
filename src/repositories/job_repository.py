from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Job as JobModel
from repositories.response_repository import ResponseModel
from repositories.user_repository import UserModel
from storage.sqlalchemy.tables import Job
from tools.updater import update_model
from web.schemas.job import JobCreateSchema, JobUpdateSchema


class JobRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, job_create_dto: JobCreateSchema) -> JobModel:
        async with self.session() as session:
            job = Job(
                user_id=job_create_dto.user_id,
                title=job_create_dto.title,
                description=job_create_dto.description,
                salary_from=job_create_dto.salary_from,
                salary_to=job_create_dto.salary_to,
                is_active=job_create_dto.is_active,
                created_at=datetime.utcnow(),
            )

            session.add(job)
            await session.commit()
            await session.refresh(job)

        return self.__to_job_model(job_from_db=job, include_relations=False)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> JobModel:
        async with self.session() as session:
            query = select(Job).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(Job.user), selectinload(Job.responses))

            res = await session.execute(query)
            job_from_db = res.scalars().first()
        job_model = self.__to_job_model(
            job_from_db=job_from_db, include_relations=include_relations
        )
        return job_model

    async def retrieve_many(
        self, limit: int = 100, skip: int = 0, include_relations: bool = False
    ) -> list[JobModel]:
        async with self.session() as session:
            query = select(Job).limit(limit).offset(skip)
            if include_relations:
                query = query.options(selectinload(Job.user)).options(selectinload(Job.responses))

            res = await session.execute(query)
            jobs_from_db = res.scalars().all()

        job_models = []
        for job in jobs_from_db:
            model = self.__to_job_model(job_from_db=job, include_relations=include_relations)
            job_models.append(model)

        return job_models

    async def update(self, id: int, job_update_dto: JobUpdateSchema) -> JobModel:
        async with self.session() as session:
            query = select(Job).filter_by(id=id).limit(1)
            res = await session.execute(query)
            job_from_db = res.scalars().first()

            if not job_from_db:
                raise ValueError("Вакансия не найдена")

            update_data = job_update_dto.model_dump(exclude_unset=True)
            update_model(job_from_db, update_data)

            session.add(job_from_db)
            await session.commit()
            await session.refresh(job_from_db)

        new_job = self.__to_job_model(job_from_db, include_relations=False)
        return new_job

    async def delete(self, id: int):
        async with self.session() as session:
            query = delete(Job).where(Job.id == id)
            res = await session.execute(query)
            await session.commit()

            if res.rowcount == 0:
                raise ValueError("Вакансия не найдена")

        return None

    @staticmethod
    def __to_job_model(job_from_db: Job, include_relations: bool = False) -> JobModel:
        job_model = None

        if job_from_db:
            if include_relations:
                if job_from_db.user:
                    job_user = UserModel(
                        id=job_from_db.user.id,
                        name=job_from_db.user.name,
                        email=job_from_db.user.email,
                        is_company=job_from_db.user.is_company,
                    )
                if job_from_db.responses:
                    job_responses = [
                        ResponseModel(
                            id=response.id,
                            job_id=response.job_id,
                            user_id=response.user_id,
                            message=response.message,
                        )
                        for response in job_from_db.responses
                    ]
            job_model = JobModel(
                id=job_from_db.id,
                user_id=job_from_db.user_id,
                title=job_from_db.title,
                description=job_from_db.description,
                salary_from=job_from_db.salary_from,
                salary_to=job_from_db.salary_to,
                is_active=job_from_db.is_active,
                created_at=job_from_db.created_at,
            )
            return job_model

        return None
