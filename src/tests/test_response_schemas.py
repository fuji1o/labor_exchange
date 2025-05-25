import pytest
from pydantic import ValidationError

from web.schemas.response import ResponseCreateSchema, ResponseUpdateSchema


def test_create_response_valid():
    schema = ResponseCreateSchema(job_id=1, user_id=1, message="Отклик")
    assert schema.job_id == 1
    assert schema.user_id == 1
    assert schema.message == "Отклик"


def test_create_response_without_message():
    schema = ResponseCreateSchema(job_id=1, user_id=1)
    assert schema.message is None


def test_update_response_valid():
    schema = ResponseUpdateSchema(message="Новое сообщение")
    assert schema.message == "Новое сообщение"
