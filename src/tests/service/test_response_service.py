import pytest

from services.exseptions import ResponseNotFoundError
from services.response import ResponseService
from tests.fakes.fake_response_repo import FakeResponseRepository
from web.schemas.response import ResponseCreateSchema


@pytest.fixture
def fake_response_service():
    repo = FakeResponseRepository()
    service = ResponseService(repo)
    return service


@pytest.mark.asyncio
async def test_create_response_success(fake_response_service):
    dto = ResponseCreateSchema(job_id=1, user_id=11, message="Здравствуйте")
    response = await fake_response_service.create(is_company=False, response_create_dto=dto)
    assert response.user_id == 11
    assert response.message == "Здравствуйте"


@pytest.mark.asyncio
async def test_create_response_permission_error(fake_response_service):
    dto = ResponseCreateSchema(job_id=1, user_id=11, message="...")
    with pytest.raises(PermissionError):
        await fake_response_service.create(is_company=True, response_create_dto=dto)


@pytest.mark.asyncio
async def test_retrieve_response_success_by_applicant(fake_response_service):
    dto = ResponseCreateSchema(job_id=1, user_id=10, message="...")
    response = await fake_response_service.create(is_company=False, response_create_dto=dto)
    retrieved = await fake_response_service.retrieve(user_id=10, is_company=False, id=response.id)
    assert retrieved.id == response.id


@pytest.mark.asyncio
async def test_retrieve_response_success_by_employer(fake_response_service):
    dto = ResponseCreateSchema(job_id=1, user_id=22, message=".....")
    response = await fake_response_service.create(is_company=False, response_create_dto=dto)

    retrieved = await fake_response_service.retrieve(user_id=999, is_company=True, id=response.id)
    assert retrieved.id == response.id


@pytest.mark.asyncio
async def test_retrieve_response_permission_error(fake_response_service):
    dto = ResponseCreateSchema(job_id=1, user_id=77, message="gggg")
    response = await fake_response_service.create(is_company=False, response_create_dto=dto)
    with pytest.raises(PermissionError):
        await fake_response_service.retrieve(user_id=777, is_company=True, id=response.id)


@pytest.mark.asyncio
async def test_delete_response_success(fake_response_service):
    dto = ResponseCreateSchema(job_id=3, user_id=303, message="bye")
    response = await fake_response_service.create(is_company=False, response_create_dto=dto)

    await fake_response_service.delete(id=response.id, user_id=303)

    with pytest.raises(ResponseNotFoundError):
        await fake_response_service.retrieve(user_id=303, is_company=False, id=response.id)
