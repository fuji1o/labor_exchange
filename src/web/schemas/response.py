from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models import Job as JobModel
from models import User as UserModel


class ResponsneCreateSchema(BaseModel):
    id: int
    job_id: int
    user_id: int
    message: str


class ResponseUpdateSchema(BaseModel):
    # сопроводительное письмо можно изменить только до того, как работодатель посмотрит его
    message: str


class ResponseSchema(BaseModel):
    id: int
    job_id: int
    user_id: int
    message: str
    user: Optional[UserModel] = None
    job: Optional[JobModel] = None
