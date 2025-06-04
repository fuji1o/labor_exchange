from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import ServicesContainer
from models import User
from services.exseptions import JobNotFoundError
from services.job import JobService
from web.schemas.job import JobCreateSchema, JobSchema, JobUpdateSchema

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
@inject
async def read_jobs(
    limit: int = 100,
    skip: int = 0,
    job_service: JobService = Depends(Provide[ServicesContainer.job_service]),
) -> list[JobSchema]:
    jobs_model = await job_service.retrieve_many(limit=limit, skip=skip)

    return [
        JobSchema(
            id=job.id,
            title=job.title,
            description=job.description,
            user_id=job.user_id,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
        )
        for job in jobs_model
    ]


@router.get("/{job_id}")
@inject
async def read_job(
    job_id: int,
    job_service: JobService = Depends(Provide[ServicesContainer.job_service]),
) -> JobSchema:
    try:
        job = await job_service.retrieve(id=job_id)
        return JobSchema(
            id=job.id,
            title=job.title,
            description=job.description,
            user_id=job.user_id,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
        )
    except JobNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")


@router.post("")
@inject
async def create_job(
    job_create_dto: JobCreateSchema,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends(Provide[ServicesContainer.job_service]),
) -> JobSchema:
    try:
        job = await job_service.create(
            user_id=current_user.id,
            is_company=current_user.is_company,
            job_create_dto=job_create_dto,
        )
        return JobSchema(
            id=job.id,
            title=job.title,
            description=job.description,
            user_id=job.user_id,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
        )
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав")


@router.put("/{job_id}")
@inject
async def update_job(
    job_id: int,
    job_update_dto: JobUpdateSchema,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends(Provide[ServicesContainer.job_service]),
) -> JobSchema:
    try:
        job = await job_service.update(
            id=job_id, job_update_dto=job_update_dto, user_id=current_user.id
        )
        return JobSchema(
            id=job.id,
            title=job.title,
            description=job.description,
            user_id=job.user_id,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
        )
    except JobNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав")


@router.delete("/{job_id}")
@inject
async def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends(Provide[ServicesContainer.job_service]),
) -> None:
    try:
        await job_service.delete(id=job_id, user_id=current_user.id)
    except JobNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав")
