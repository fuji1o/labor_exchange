from decimal import Decimal

import pytest
from pydantic import ValidationError

from web.schemas.job import JobCreateSchema, JobUpdateSchema


def test_create_job_valid():
    job = JobCreateSchema(
        title="Driver",
        description="Bus driver",
        salary_from=Decimal("30000"),
        salary_to=Decimal("40000"),
    )
    assert job.title == "Driver"
    assert job.salary_from == Decimal("30000")
    assert job.is_active is True


def test_create_job_invalid_salary_range():
    with pytest.raises(ValidationError) as exc:
        JobCreateSchema(
            title="Driver",
            description="Bus driver",
            salary_from=Decimal("40000"),
            salary_to=Decimal("30000"),
        )
    assert "з/п_от не может быть больше з/п_до" in str(exc.value)


def test_update_job_valid_salary_range():
    job = JobUpdateSchema(
        salary_from=Decimal("30000"),
        salary_to=Decimal("40000"),
    )
    assert job


def test_update_job_invalid_salary_range():
    with pytest.raises(ValidationError):
        JobUpdateSchema(
            salary_from=Decimal("70000"),
            salary_to=Decimal("20000"),
        )
