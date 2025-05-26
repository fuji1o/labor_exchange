from interfaces.i_repository import IRepositoryAsync
from services.base_service import BaseService
from services.exseptions import UserAlreadyExistsError, UserNotFoundError
from tools.security import hash_password
from web.schemas import UserCreateSchema, UserUpdateSchema


class UserService(BaseService):
    def __init__(self, user_repository: IRepositoryAsync):
        super().__init__(user_repository)

    async def create(self, user_create_dto: UserCreateSchema):
        existing_user = await self.repository.retrieve(email=user_create_dto.email)
        if existing_user:
            raise UserAlreadyExistsError("Пользователь с таким email уже существует")

        hashed_password = hash_password(user_create_dto.password)
        copy_dto = user_create_dto.model_copy(update={"password": hashed_password})

        return await self.repository.create(copy_dto)

    async def retrieve(self, **kwargs):
        user = await super().retrieve(**kwargs)
        if not user:
            raise UserNotFoundError("Пользователь не найден")
        return user

    async def retrieve_many(self, limit: int = 100, skip: int = 0):
        return await super().retrieve_many(limit=limit, skip=skip)

    async def update(self, id: int, user_update_dto: UserUpdateSchema, current_user_id: int):
        if id != current_user_id:
            raise PermissionError("Недостаточно прав для обновления профиля")

        return await self.repository.update(id=id, user_update_dto=user_update_dto)

    async def delete(self, id: int, current_user_id: int):
        return await self.delete_with_permission_check(
            id=id,
            user_id=current_user_id,
            get_owner_id=lambda user: user.id,
            not_found_exc=UserNotFoundError("Пользователь не найден"),
        )
