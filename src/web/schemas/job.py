from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from tools.salary_validation import SalaryValidation



class JobCreateSchema(SalaryValidation,BaseModel):
    title: str = Field(..., description="Название вакансии")
    description: str = Field(..., description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(default=None, description="Минимальная зарплата")
    salary_to: Optional[Decimal] = Field(default=None, description="Максимальная зарплата")
    is_active: Optional[bool] = Field(default=True, description="Актуальность вакансии")

    

class JobUpdateSchema(SalaryValidation, BaseModel):
    title: str = Field(None, description="Название вакансии")
    description: str = Field(None, description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(None, description="Минимальная зарплата")
    salary_to: Optional[Decimal] = Field(None, description="Максимальная зарплата")
    is_active: Optional[bool] = Field(None, description="Актуальность вакансии")



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
