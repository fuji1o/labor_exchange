from typing import Any, Callable

from interfaces.i_repository import IRepositoryAsync


class BaseService:
    def __init__(self, repository: IRepositoryAsync):
        self.repository = repository

    async def retrieve(self, **kwargs):
        return await self.repository.retrieve(**kwargs)

    async def retrieve_many(self, limit: int = 100, skip: int = 0):
        return await self.repository.retrieve_many(limit=limit, skip=skip)

    async def delete_with_permission_check(
        self, id: int, user_id: int, get_owner_id: Callable[[Any], int], not_found_exc: Exception
    ):
        instance = await self.repository.retrieve(id=id)
        if not instance:
            raise not_found_exc

        if get_owner_id(instance) != user_id:
            raise PermissionError("Недостаточно прав")

        return await self.repository.delete(id=id)
