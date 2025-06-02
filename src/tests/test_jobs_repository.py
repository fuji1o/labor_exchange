import pytest
from pydantic import ValidationError

from tools.fixtures.jobs import JobFactory
from tools.fixtures.users import UserFactory
from web.schemas.job import JobCreateSchema, JobUpdateSchema


@pytest.mark.asyncio
async def test_get_all_jobs(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        session.flush()

    all_jobs = await job_repository.retrieve_many()
    assert all_jobs
    assert len(all_jobs) == 1

    job_from_repo = all_jobs[0]
    assert job_from_repo.id == job.id
    assert job_from_repo.title == job.title


@pytest.mark.asyncio
async def test_get_job_by_id(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        await session.flush()

    retrieved_job = await job_repository.retrieve(id=job.id)
    assert retrieved_job is not None
    assert retrieved_job.id == job.id


@pytest.mark.asyncio
async def test_create_job(job_repository, sa_session):
    async with sa_session() as session:
        user = UserFactory.build()
        session.add(user)
        session.flush()

    job_data = JobCreateSchema(
        title="Electrician",
        description="full-time job",
        salary_from=50000,
        salary_to=100000,
        is_active=True,
        user_id=user.id,
    )

    new_job = await job_repository.create(job_data)
    assert new_job is not None
    assert new_job.title == job_data.title
    assert new_job.user_id == user.id


@pytest.mark.asyncio
async def test_update_job(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        await session.flush()

    update_data = JobUpdateSchema(title="Новое название")
    updated_job = await job_repository.update(id=job.id, job_update_dto=update_data)

    assert updated_job.id == job.id
    assert updated_job.title == "Новое название"


@pytest.mark.asyncio
async def test_create_job_invalid_salary_range(job_repository, sa_session):
    async with sa_session() as session:
        user = UserFactory.build()
        session.add(user)
        await session.flush()

    with pytest.raises(ValidationError):
        JobCreateSchema(
            title="PPP",
            description="LLL",
            salary_from=100_000,
            salary_to=50_000,
            is_active=True,
            user_id=user.id,
        )


@pytest.mark.asyncio
async def test_update_non_existing_job(job_repository):
    with pytest.raises(ValueError, match="Вакансия не найдена"):
        await job_repository.update(id=9999, job_update_dto=JobUpdateSchema(title="Nope"))


@pytest.mark.asyncio
async def test_delete_job(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        await session.flush()

    await job_repository.delete(id=job.id)
    result = await job_repository.retrieve(id=job.id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_non_existing_job(job_repository):
    with pytest.raises(ValueError, match="Вакансия не найдена"):
        await job_repository.delete(id=9999)
