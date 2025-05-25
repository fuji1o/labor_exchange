from interfaces.i_repository import IRepositoryAsync
from services.exseptions import JobNotFoundError
from web.schemas.job import JobCreateSchema, JobUpdateSchema


class JobService:
    def __init__(self, job_repository: IRepositoryAsync):
        self.job_repository = job_repository

    async def create(self, is_company: bool, job_create_dto: JobCreateSchema):
        if not is_company:
            raise PermissionError("Недостаточно прав")
        return await self.job_repository.create(job_create_dto=job_create_dto)

    async def retrieve(self, **kwargs):
        try:
            return await self.job_repository.retrieve(**kwargs)
        except:
            raise JobNotFoundError("Вакансия не найдена")

    async def retrieve_many(self, limit: int, skip: int):
        return await self.job_repository.retrieve_many(limit=limit, skip=skip)

    async def update(self, id: int, job_update_dto: JobUpdateSchema, user_id: int):
        job = await self.job_repository.retrieve(id=id)
        if not job:
            raise JobNotFoundError("Вакансия не найдена")
        if job.user.id != user_id:
            raise PermissionError("Недостаточно прав")
        return await self.job_repository.update(id=id, job_update_dto=job_update_dto)

    async def delete(self, id: int, user_id: int):
        job = await self.job_repository.retrieve(id=id)
        if not job:
            raise JobNotFoundError("Вакансия не найдена")

        if job.user.id != user_id:
            raise PermissionError("Недостаточно прав")

        return await self.job_repository.delete(id=id)
