from interfaces.i_repository import IRepositoryAsync
from services.exseptions import ResponseNotFoundError
from web.schemas.response import ResponseCreateSchema, ResponseUpdateSchema


class ResponseService:
    def __init__(self, response_repository: IRepositoryAsync):
        self.response_repository = response_repository

    async def create(self, is_company: bool, response_create_dto: ResponseCreateSchema):
        if is_company:
            raise PermissionError("Откликаться могут только соискатели")

        return await self.response_repository.create(response_create_dto)

    async def retrieve(self, **kwargs):
        response = await self.response_repository.retrieve(**kwargs)
        if not response:
            raise ResponseNotFoundError("Отклик не найден")
        return response

    async def retrieve_many(self, limit: int, skip: int):
        return await self.response_repository.retrieve_many(limit=limit, skip=skip)

    async def update(self, id: int, response_update_dto: ResponseUpdateSchema, user_id: int):
        response = await self.response_repository.retrieve(id=id)
        if not response:
            raise ResponseNotFoundError("Отклик не найден")

        if response.user_id != user_id:
            raise PermissionError("Недостаточно прав для изменения отклика")
        
        updated_response = await self.response_repository.update(id=id, response_update_dto=response_update_dto)
        return updated_response

    async def delete(self, id: int, user_id: int):
        response = await self.response_repository.retrieve(id=id)
        if not response:
            raise ResponseNotFoundError("Отклик не найден")

        if response.user_id != user_id:
            raise PermissionError("Недостаточно прав для удаления отклика")

        return await self.response_repository.delete(id=id)
