from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import ServicesContainer
from models import User
from repositories import UserRepository
from services.exseptions import UserAlreadyExistsError, UserNotFoundError
from services.user import UserService
from tools.security import hash_password
from web.schemas import UserCreateSchema, UserSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
@inject
async def read_users(
    limit: int = 100,
    skip: int = 0,
    user_service: UserService = Depends(Provide[ServicesContainer.user_service]),
    current_user: User = Depends(get_current_user),
) -> list[UserSchema]:
    users_model = await user_service.retrieve_many(limit, skip)

    return [
        UserSchema(id=model.id, name=model.name, email=model.email, is_company=model.is_company)
        for model in users_model
        if model.id == current_user.id or model.is_company
    ]


@router.get("/{user_id}")
@inject
async def read_user(
    user_id: int,
    user_service: UserService = Depends(Provide[ServicesContainer.user_service]),
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав")

    try:
        user_model = await user_service.retrieve(id=user_id)
        return UserSchema(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            is_company=user_model.is_company,
        )
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.post("")
@inject
async def create_user(
    user_create_dto: UserCreateSchema,
    user_service: UserService = Depends(Provide[ServicesContainer.user_service]),
) -> UserSchema:
    try:
        user = await user_service.create(user_create_dto)
        return UserSchema(**asdict(user))
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже существует"
        )


@router.put("/{id}")
@inject
async def update_user(
    user_update_schema: UserUpdateSchema,
    user_service: UserService = Depends(Provide[ServicesContainer.user_service]),
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    try:
        updated_user = await user_service.update(
            user_id=current_user.id,
            user_update_dto=user_update_schema,
        )
        return UserSchema(**asdict(updated_user))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав")
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.delete("/{id}")
@inject
async def delete_user(
    user_service: UserService = Depends(Provide[ServicesContainer.user_service]),
    current_user: User = Depends(get_current_user),
) -> None:
    try:
        await user_service.delete(id=current_user.id, current_user_id=current_user.id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return
