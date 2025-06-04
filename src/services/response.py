from interfaces.i_repository import IRepositoryAsync
from services.base_service import BaseService
from services.exseptions import ResponseNotFoundError
from web.schemas.response import ResponseCreateSchema, ResponseUpdateSchema


class ResponseService(BaseService):
    def __init__(self, response_repository: IRepositoryAsync):
        super().__init__(response_repository)

    async def create(self, is_company: bool, response_create_dto: ResponseCreateSchema):
        if is_company:
            raise PermissionError("Откликаться могут только соискатели")

        return await self.repository.create(response_create_dto)

    async def retrieve(self, *, user_id: int, is_company: bool, id: int):
        response = await self.repository.retrieve(id=id)
        if not response:
            raise ResponseNotFoundError("Отклик не найден")

        if is_company:
            if not hasattr(response, "job") or response.job.user_id != user_id:
                raise PermissionError("Нет доступа к отклику (работодатель не владелец вакансии)")
        else:
            if response.user_id != user_id:
                raise PermissionError("Нет доступа к отклику (не ваш отклик)")

        return response

    async def retrieve_many(self, limit: int, skip: int):
        return await super().retrieve_many(limit=limit, skip=skip)

    async def update(self, id: int, response_update_dto: ResponseUpdateSchema, user_id: int):
        response = await self.repository.retrieve(id=id)
        if not response:
            raise ResponseNotFoundError("Отклик не найден")

        if response.user_id != user_id:
            raise PermissionError("Недостаточно прав для изменения отклика")

        return await self.repository.update(id=id, response_update_dto=response_update_dto)

    async def delete(self, id: int, user_id: int):
        await self.delete_with_permission_check(
            id=id,
            user_id=user_id,
            get_owner_id=lambda resp: resp.user_id,
            not_found_exc=ResponseNotFoundError("Отклик не найден"),
        )
