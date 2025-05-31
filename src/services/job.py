from interfaces.i_repository import IRepositoryAsync
from services.base_service import BaseService
from services.exseptions import JobNotFoundError
from web.schemas.job import JobCreateSchema, JobUpdateSchema


class JobService(BaseService):
    def __init__(self, job_repository: IRepositoryAsync):
        super().__init__(job_repository)

    async def create(self, is_company: bool, job_create_dto: JobCreateSchema):
        if not is_company:
            raise PermissionError("Недостаточно прав")
        return await self.repository.create(job_create_dto=job_create_dto)

    async def retrieve(self, **kwargs):
        job = await super().retrieve(**kwargs)
        if not job:
            raise JobNotFoundError("Вакансия не найдена")
        return job

    async def retrieve_many(self, limit: int, skip: int):
        return await super().retrieve_many(limit=limit, skip=skip)

    async def update(self, id: int, job_update_dto: JobUpdateSchema, user_id: int):
        job = await self.repository.retrieve(id=id)
        if not job:
            raise JobNotFoundError("Вакансия не найдена")
        if job.user.id != user_id:
            raise PermissionError("Недостаточно прав")
        return await self.repository.update(id=id, job_update_dto=job_update_dto)

    async def delete(self, id: int, user_id: int):
        return await self.delete_with_permission_check(
            id=id,
            user_id=user_id,
            get_owner_id=lambda job: job.user.id,
            not_found_exc=JobNotFoundError("Вакансия не найдена"),
        )
