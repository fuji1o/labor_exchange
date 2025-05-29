from decimal import Decimal

import pytest
from pydantic import ValidationError

from web.schemas.job import JobCreateSchema


def test_create_job_invalid_salary_range():
    with pytest.raises(ValidationError) as exc:
        JobCreateSchema(
            title="Driver",
            description="Bus driver",
            salary_from=Decimal("40000"),
            salary_to=Decimal("30000"),
        )
    assert "з/п_от не может быть больше з/п_до" in str(exc.value)
