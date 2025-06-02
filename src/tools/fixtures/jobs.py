from datetime import datetime

import factory

from storage.sqlalchemy.tables import Job
from tools.fixtures.users import UserFactory


class JobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Job

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("job")
    description = factory.Faker("paragraph")
    salary_from = factory.Faker("random_int", min=20000, max=80000)
    salary_to = factory.Faker("random_int", min=50000, max=100000)
    is_active = True
    created_at = factory.LazyFunction(datetime.utcnow)
