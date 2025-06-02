from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import ServicesContainer
from models import User
from services.exseptions import ResponseNotFoundError
from services.response import ResponseService
from web.schemas.response import ResponseCreateSchema, ResponseSchema, ResponseUpdateSchema

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("")
@inject
async def read_responses(
    limit: int = 100,
    skip: int = 0,
    current_user: User = Depends(get_current_user),
    response_service: ResponseService = Depends(Provide[ServicesContainer.response_service]),
) -> list[ResponseSchema]:
    responses_model = await response_service.retrieve_many(limit=limit, skip=skip)

    filtered_responses = []

    for resp in responses_model:
        if not current_user.is_company and resp.user_id != current_user.id:
            continue
        if current_user.is_company and resp.job.user.id != current_user.id:
            continue
        filtered_responses.append(ResponseSchema(**asdict(resp)))

    return filtered_responses


@router.get("/{response_id}")
@inject
async def read_response(
    response_id: int,
    current_user: User = Depends(get_current_user),
    response_service: ResponseService = Depends(Provide[ServicesContainer.response_service]),
) -> ResponseSchema:
    try:
        resp = await response_service.retrieve(id=response_id)

        if not current_user.is_company and resp.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к отклику"
            )

        if current_user.is_company and resp.job.user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к отклику"
            )

        return ResponseSchema(**asdict(resp))

    except ResponseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_response(
    response_create_dto: ResponseCreateSchema,
    current_user: User = Depends(get_current_user),
    response_service: ResponseService = Depends(Provide[ServicesContainer.response_service]),
) -> ResponseSchema:
    try:
        response = await response_service.create(
            is_company=current_user.is_company,
            response_create_dto=response_create_dto,
        )
        return ResponseSchema(**asdict(response))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")


@router.put("/{response_id}")
@inject
async def update_response(
    response_id: int,
    response_update_dto: ResponseUpdateSchema,
    current_user: User = Depends(get_current_user),
    response_service: ResponseService = Depends(Provide[ServicesContainer.response_service]),
) -> ResponseSchema:
    try:
        response = await response_service.update(
            id=response_id,
            response_update_dto=response_update_dto,
            user_id=current_user.id,
        )
        return ResponseSchema(**asdict(response))
    except ResponseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")


@router.delete("/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_response(
    response_id: int,
    current_user: User = Depends(get_current_user),
    response_service: ResponseService = Depends(Provide[ServicesContainer.response_service]),
) -> None:
    try:
        await response_service.delete(id=response_id, user_id=current_user.id)
    except ResponseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
