from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class JobCreateSchema(BaseModel):
    title: str = Field(..., description="Название вакансии")
    description: str = Field(..., description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(default=None, description="Минимальная зарплата")
    salary_to: Optional[Decimal] = Field(default=None, description="Максимальная зарплата")
    is_active: Optional[bool] = Field(default=True, description="Актуальность вакансии")

    @model_validator(mode="after")
    def validate_salary_range(self) -> Self:
        if self.salary_from is not None and self.salary_to is not None:
            if self.salary_from > self.salary_to:
                raise ValueError("з/п_от не может быть больше з/п_до")
        return self


class JobUpdateSchema(BaseModel):
    title: str = Field(None, description="Название вакансии")
    description: str = Field(None, description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(None, description="Минимальная зарплата")
    salary_to: Optional[Decimal] = Field(None, description="Максимальная зарплата")
    is_active: Optional[bool] = Field(None, description="Актуальность вакансии")

    @model_validator(mode="after")
    def validate_salary_range(self) -> Self:
        if self.salary_from is not None and self.salary_to is not None:
            if self.salary_from > self.salary_to:
                raise ValueError("з/п_от не может быть больше з/п_до")
        return self


class JobSchema(BaseModel):
    id: int = Field(..., description="Идентификатор вакансии")
    user_id: int = Field(..., description="Идентификатор пользователя")
    title: str = Field(..., description="Название вакансии")
    description: str = Field(..., description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(None, description="Минимальная зарплата")
    salary_to: Optional[Decimal] = Field(None, description="Максимальная зарплата")
    is_active: bool = Field(default=True, description="Актуальность вакансии")

    class Config:
        from_attributes = True
