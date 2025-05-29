from typing import Any


class FakeUserRepository:
    def __init__(self):
        self._users = []
        self._id = 1

    async def create(self, user_create_dto: Any, hashed_password: str = None):
        user = {
            "id": self._id,
            "name": user_create_dto.name,
            "email": user_create_dto.email,
            "is_company": user_create_dto.is_company,
            "password": hashed_password,
            "password2": hashed_password,
        }
        self._users.append(user)
        self._id += 1
        return user

    async def retrieve(self, **kwargs):
        for user in self._users:
            if all(user.get(k) == v for k, v in kwargs.items()):
                return user

        return None

    async def retrieve_many(self, limit: int = 100, skip: int = 0):
        return self._users[skip : skip + limit]

    async def update(self, id: int, user_update_dto: Any):
        for user in self._users:
            if user["id"] == id:
                for key, value in user_update_dto.model_dump().items():
                    if value is not None:
                        user[key] = value
                return user
        return None

    async def delete(self, id: int):
        for user in self._users:
            if user["id"] == id:
                self._users.remove(user)
                return True
        return False
