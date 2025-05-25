from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_model(orm_instanse: object, data_class: type[T]) -> T:
    return data_class.model_validate(orm_instanse)
