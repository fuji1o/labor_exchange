import pytest

from services.exseptions import UserAlreadyExistsError, UserNotFoundError
from services.user import UserService
from tests.fakes.fake_user_repo import FakeUserRepository
from web.schemas import UserCreateSchema, UserUpdateSchema


@pytest.fixture
def fake_service():
    repo = FakeUserRepository()
    service = UserService(repo)
    return service


@pytest.mark.asyncio
async def test_create_user_already_exists(fake_service):
    user_dto = UserCreateSchema(
        name="John",
        email="j@example.ru",
        password="11111111",
        password2="11111111",
        is_company=False,
    )
    await fake_service.create(user_dto)

    with pytest.raises(UserAlreadyExistsError):
        await fake_service.create(user_dto)


@pytest.mark.asyncio
async def test_retrieve_user_success(fake_service):
    user_dto = UserCreateSchema(
        name="Emily",
        email="e@example.com",
        password="22222222",
        password2="22222222",
        is_company=False,
    )
    created_user = await fake_service.create(user_dto)

    user = await fake_service.retrieve(id=created_user["id"])
    assert user["id"] == created_user["id"]


@pytest.mark.asyncio
async def test_retrieve_user_not_found(fake_service):
    with pytest.raises(UserNotFoundError):
        await fake_service.retrieve(id=9999)


@pytest.mark.asyncio
async def test_update_user_success(fake_service):
    user_dto = UserCreateSchema(
        name="Carla",
        email="c@gmail.com",
        password="33333333",
        password2="33333333",
        is_company=False,
    )
    created = await fake_service.create(user_dto)
    update_dto = UserUpdateSchema(name="New Carla")
    updated = await fake_service.update(
        id=created["id"], user_update_dto=update_dto, current_user_id=created["id"]
    )
    assert updated["name"] == "New Carla"


@pytest.mark.asyncio
async def test_update_user_denied(fake_service):
    user_dto = UserCreateSchema(
        name="Eliot",
        email="el@gmail.com",
        password="33333333",
        password2="33333333",
        is_company=False,
    )
    created = await fake_service.create(user_dto)
    update_dto = UserUpdateSchema(name="Not Eliot")
    with pytest.raises(PermissionError):
        await fake_service.update(id=created["id"], user_update_dto=update_dto, current_user_id=999)


@pytest.mark.asyncio
async def test_delete_user_success(fake_service):
    user_dto = UserCreateSchema(
        name="Terk",
        email="t@example.com",
        password="77777777",
        password2="77777777",
        is_company=False,
    )
    created = await fake_service.create(user_dto)

    result = await fake_service.delete(id=created["id"], current_user_id=created["id"])
    assert result is True

    with pytest.raises(UserNotFoundError):
        await fake_service.retrieve(id=created["id"])


@pytest.mark.asyncio
async def test_delete_user_permission_denied(fake_service):
    user_dto = UserCreateSchema(
        name="Kelso",
        email="k@example.com",
        password="99999999",
        password2="99999999",
        is_company=False,
    )
    created = await fake_service.create(user_dto)

    with pytest.raises(PermissionError):
        await fake_service.delete(id=created["id"], current_user_id=999)
