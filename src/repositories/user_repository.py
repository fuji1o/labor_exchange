from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import User as UserModel
from storage.sqlalchemy.tables import User
from tools.converter import to_model
from tools.updater import update_model
from web.schemas import UserCreateSchema, UserUpdateSchema


class UserRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, user_create_dto: UserCreateSchema, hashed_password: str) -> UserModel:
        async with self.session() as session:
            user = User(
                name=user_create_dto.name,
                email=user_create_dto.email,
                is_company=user_create_dto.is_company,
                hashed_password=hashed_password,
            )

            session.add(user)
            await session.commit()
            await session.refresh(user)

        return to_model(user, UserModel)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> UserModel:
        async with self.session() as session:
            query = select(User).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(User.jobs)).options(selectinload(User.responses))

            res = await session.execute(query)
            user_from_db = res.scalars().first()

        user_model = to_model(user_from_db, UserModel)
        return user_model

    async def retrieve_many(
        self, limit: int = 100, skip: int = 0, include_relations: bool = False
    ) -> list[UserModel]:
        async with self.session() as session:
            query = select(User).limit(limit).offset(skip)
            if include_relations:
                query = query.options(selectinload(User.jobs)).options(selectinload(User.responses))

            res = await session.execute(query)
            users_from_db = res.scalars().all()

        users_model = []
        for user in users_from_db:
            model = to_model(user, UserModel)
            users_model.append(model)

        return users_model

    async def update(self, id: int, user_update_dto: UserUpdateSchema) -> UserModel:
        async with self.session() as session:
            query = select(User).filter_by(id=id).limit(1)
            res = await session.execute(query)
            user_from_db = res.scalars().first()

            if not user_from_db:
                raise ValueError("Пользователь не найден")

            update_data = user_update_dto.model_dump(exclude_unset=True)
            update_model(user_from_db, update_data)

            session.add(user_from_db)
            await session.commit()
            await session.refresh(user_from_db)

        new_user = to_model(user_from_db, UserModel)
        return new_user

    """async def delete(self, id: int):
        async with self.session() as session:
            query = select(User).filter_by(id=id).limit(1)
            res = await session.execute(query)
            user_from_db = res.scalars().first()

            if user_from_db:
                await session.delete(user_from_db)
                await session.commit()
            else:
                raise ValueError("Пользователь не найден")

        return to_model(user_from_db, UserModel)
        """

    async def delete(self, id: int):
        async with self.session() as session:
            query = delete(User).where(User.id == id)
            res = await session.execute(query)
            await session.commit()

            if res.rowcount == 0:
                raise ValueError("Пользователь не найден")

        return None 
