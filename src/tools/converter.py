from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_model(orm_instanse: object, data_class: type[T]) -> T:
    if orm_instanse is None:
        return None

    if isinstance(orm_instanse, list):
        return [data_class.model_validate(obj) for obj in orm_instanse]

    return data_class.from_orm(orm_instanse)
