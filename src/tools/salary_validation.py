from pydantic import BaseModel, model_validator
from typing_extensions import Self


class SalaryValidation(BaseModel):
    @model_validator(mode="after")
    def validate_salary_range(self) -> Self:
        if self.salary_from is not None and self.salary_to is not None:
            if self.salary_from > self.salary_to:
                raise ValueError("з/п_от не может быть больше з/п_до")
        return self
