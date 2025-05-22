from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Job: 
    id: int
    user_id: int
    title: str
    description: str
    salary_from: Decimal
    salary_to: Decimal
    is_active: bool
    created_at: datetime

    responses: list[Response] = field(default_factory=list)