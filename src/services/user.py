from interfaces.i_repository import IRepositoryAsync
from services.exseptions import UserAlreadyExistsError, UserNotFoundError
from tools.security import hash_password
from web.schemas import UserCreateSchema, UserUpdateSchema


class UserService:
    def __init__(self, user_repository: IRepositoryAsync):
        self.user_repository = user_repository

    async def create(self, user_create_dto: UserCreateSchema):
        existing_user = await self.user_repository.retrieve(email=user_create_dto.email)
        if existing_user:
            raise UserAlreadyExistsError("Пользователь с таким email уже существует")

        return await self.user_repository.create(
            user_create_dto=user_create_dto, hashed_password=hash_password(user_create_dto.password)
        )

    async def retrieve(self, **kwargs):
        user = await self.user_repository.retrieve(**kwargs)
        if not user:
            raise UserNotFoundError("Пользователь не найден")
        return user

    async def retrieve_many(self, limit: int = 100, skip: int = 0):
        return await self.user_repository.retrieve_many(limit=limit, skip=skip)

    async def update(self, id: int, user_update_dto: UserUpdateSchema, current_user_id: int):
        if id != current_user_id:
            raise PermissionError("Недостаточно прав для обновления профиля")

        return await self.user_repository.update(id=id, user_update_dto=user_update_dto)

    async def delete(self, id: int, current_user_id: int):
        if id != current_user_id:
            raise PermissionError("Недостаточно прав для удаления профиля")

        return await self.user_repository.delete(id=id)
