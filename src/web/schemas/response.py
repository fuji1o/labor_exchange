from typing import Optional

from pydantic import BaseModel, Field


class ResponseCreateSchema(BaseModel):
    job_id: int = Field(..., description="Идентификатор вакансии")
    user_id: int = Field(..., description="Идентификатор пользователя")
    message: Optional[str] = Field(None, description="Сопроводительное письмо")


class ResponseUpdateSchema(BaseModel):
    # сопроводительное письмо можно изменить только до того, как работодатель посмотрит его
    message: Optional[str] = Field(None, description="Сопроводительное письмо")


class ResponseSchema(BaseModel):
    job_id: int = Field(..., description="Идентификатор вакансии")
    user_id: int = Field(..., description="Идентификатор пользователя")
    message: str = Field(None, description="Сопроводительное письмо")

    class Config:
        from_attributes = True
