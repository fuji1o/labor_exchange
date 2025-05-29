import pytest

from services.exseptions import JobNotFoundError
from services.job import JobService
from tests.fakes.fake_job_repo import FakeJobRepository
from web.schemas.job import JobCreateSchema, JobUpdateSchema


@pytest.fixture
def fake_job_service():
    repo = FakeJobRepository()
    service = JobService(repo)
    return service


@pytest.mark.asyncio
async def test_create_job_success(fake_job_service):
    job_dto = JobCreateSchema(
        title="Driver",
        description="bus",
        salary_from=40000,
        salary_to=50000,
        is_active=True,
    )

    job = await fake_job_service.create(user_id=1, is_company=True, job_create_dto=job_dto)

    assert job.id == 1
    assert job.title == "Driver"


@pytest.mark.asyncio
async def test_create_job_permission_error(fake_job_service):
    job_dto = JobCreateSchema(
        title="Teacher",
        description="English",
        salary_from=40000,
        salary_to=54000,
        is_active=True,
    )

    with pytest.raises(PermissionError):
        await fake_job_service.create(user_id=2, is_company=False, job_create_dto=job_dto)


@pytest.mark.asyncio
async def test_retrieve_job_success(fake_job_service):
    job_dto = JobCreateSchema(
        title="Doctor",
        description="surgeon",
        salary_from=90000,
        salary_to=110000,
        is_active=True,
    )

    job = await fake_job_service.create(user_id=3, is_company=True, job_create_dto=job_dto)
    retrieved = await fake_job_service.retrieve(id=job.id)

    assert retrieved.id == job.id


@pytest.mark.asyncio
async def test_retrieve_job_not_found(fake_job_service):
    with pytest.raises(JobNotFoundError):
        await fake_job_service.retrieve(id=999)


@pytest.mark.asyncio
async def test_update_job_permission_error(fake_job_service):
    job_dto = JobCreateSchema(
        title="F",
        description="G",
        salary_from=70000,
        salary_to=90000,
        is_active=True,
    )
    job = await fake_job_service.create(user_id=4, is_company=True, job_create_dto=job_dto)

    update_dto = JobUpdateSchema(title="false")

    with pytest.raises(PermissionError):
        await fake_job_service.update(id=job.id, job_update_dto=update_dto, user_id=999)


@pytest.mark.asyncio
async def test_delete_job_success(fake_job_service):
    job_dto = JobCreateSchema(
        title="Dentist",
        description="...",
        salary_from=60000,
        salary_to=80000,
        is_active=True,
    )
    job = await fake_job_service.create(user_id=5, is_company=True, job_create_dto=job_dto)

    result = await fake_job_service.delete(id=job.id, user_id=5)
    assert result is True

    with pytest.raises(JobNotFoundError):
        await fake_job_service.retrieve(id=job.id)
