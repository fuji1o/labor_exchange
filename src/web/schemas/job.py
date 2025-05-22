from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, model_validator
from typing_extensions import Self


class JobCreateSchema(BaseModel):
    title: str
    description: str
    salary_from: Optional[Decimal] = None
    salary_to: Optional[Decimal] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_salary_range(self) -> Self:
        if self.salary_from is not None and self.salary_to is not None:
            if self.salary_from > self.salary_to:
                raise ValueError("з/п_от не может быть больше з/п_до")
        return self

    @model_validator(mode="after")
    def validate_created_at(self) -> Self:
        if self.created_at is not None and self.created_at > datetime.utcnow():
            raise ValueError("created_at cannot be in the future")
        return self


class JobUpdateSchema(BaseModel):
    title: str = None
    description: str = None
    salary_from: Optional[Decimal] = None
    salary_to: Optional[Decimal] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_salary_range(self) -> Self:
        if self.salary_from is not None and self.salary_to is not None:
            if self.salary_from > self.salary_to:
                raise ValueError("з/п_от не может быть больше з/п_до")
        return self


class JobSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    salary_from: Decimal
    salary_to: Decimal
    is_active: bool
    created_at: datetime
