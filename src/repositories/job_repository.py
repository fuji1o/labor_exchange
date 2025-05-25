from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Job as JobModel
from storage.sqlalchemy.tables import Job
from tools.converter import to_model
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
                created_at=job_create_dto.created_at,
            )

            session.add(job)
            await session.commit()
            await session.refresh(job)

        return to_model(job, JobModel)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> JobModel:
        async with self.session() as session:
            query = select(Job).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(Job.user), selectinload(Job.responses))

            res = await session.execute(query)
            job_from_db = res.scalars().first()

        return to_model(job_from_db, JobModel) if job_from_db else None

    async def retrieve_many(
        self, limit: int = 100, skip: int = 0, include_relations: bool = False
    ) -> list[JobModel]:
        async with self.session() as session:
            query = select(Job).limit(limit).offset(skip)
            if include_relations:
                query = query.options(selectinload(Job.user)).options(selectinload(Job.responses))

            res = await session.execute(query)
            jobs_from_db = res.scalars().all()

        return [to_model(job, JobModel) for job in jobs_from_db]

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

        return to_model(job_from_db, JobModel)

    async def delete(self, id: int):
        async with self.session() as session:
            query = delete(Job).where(Job.id == id)
            res = await session.execute(query)
            await session.commit()

            if res.rowcount == 0:
                raise ValueError("Вакансия не найдена")

        return None  # правильно ли возвращать None

    """
    async def delete(self, id: int):
        async with self.session() as session:
        job_from_db = await self.retrieve(id=id)
        if not job_from_db:
            raise ValueError("Вакансия не найдена")
        else:
            await session.delete(job_from_db)
            await session.commit()

        return to_model(job_from_db, include_relations=False)
    """
