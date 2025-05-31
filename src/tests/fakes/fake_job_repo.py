from web.schemas.job import JobCreateSchema, JobUpdateSchema


class FakeUser:
    def __init__(self, id):
        self.id = id


class FakeJob:
    def __init__(self, id, title, description, salary_from, salary_to, is_active, user_id):
        self.id = id
        self.title = title
        self.description = description
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.is_active = is_active
        self.user = FakeUser(user_id)


class FakeJobRepository:
    def __init__(self):
        self._jobs = []
        self._id = 1

    async def create(self, job_create_dto: JobCreateSchema, user_id: int):
        job = FakeJob(
            id=self._id,
            title=job_create_dto.title,
            description=job_create_dto.description,
            salary_from=job_create_dto.salary_from,
            salary_to=job_create_dto.salary_to,
            is_active=job_create_dto.is_active,
            user_id=user_id,
        )
        self._jobs.append(job)
        self._id += 1
        return job

    async def retrieve(self, include_relations: bool = False, **kwargs):
        for job in self._jobs:
            match = True
            for k, v in kwargs.items():
                if k == "id" and job.id != v:
                    match = False
                elif k == "user_id" and job.user.id != v:
                    match = False
            if match:
                return job
        return None

    async def retrieve_many(self, limit: int = 100, skip: int = 0, include_relations: bool = False):
        return self._jobs[skip : skip + limit]
    
    async def update(self, id: int, job_update_dto: JobUpdateSchema):
        for job in self._jobs:
            if job.id == id:
                update_data = job_update_dto.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(job, key, value)
                return job
        raise ValueError("Вакансия не найдена")

    async def delete(self, id: int):
        for job in self._jobs:
            if job.id == id:
                self._jobs.remove(job)
                return True
        raise ValueError("Вакансия не найдена")
