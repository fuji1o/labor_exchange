from web.schemas.response import ResponseCreateSchema, ResponseUpdateSchema


class FakeJob:
    def __init__(self, user_id):
        self.user_id = user_id


class FakeResponse:
    def __init__(self, id, job_id, user_id, message):
        self.id = id
        self.job_id = job_id
        self.user_id = user_id
        self.message = message
        self.job = FakeJob(user_id=999)


class FakeResponseRepository:
    def __init__(self):
        self._responses = []
        self._id = 1

    async def create(self, response_create_dto: ResponseCreateSchema):
        response = FakeResponse(
            id=self._id,
            job_id=response_create_dto.job_id,
            user_id=response_create_dto.user_id,
            message=response_create_dto.message,
        )
        self._responses.append(response)
        self._id += 1
        return response

    async def retrieve(self, include_relations: bool = False, **kwargs):
        for response in self._responses:
            if all(getattr(response, k) == v for k, v in kwargs.items()):
                return response
        return None

    async def retrieve_many(self, limit: int = 100, skip: int = 0, include_relations: bool = False):
        return self._responses[skip:skip + limit]

    async def update(self, id: int, response_update_dto: ResponseUpdateSchema):
        for response in self._responses:
            if response.id == id:
                if response_update_dto.message is not None:
                    response.message = response_update_dto.message
                return response
        raise ValueError("Отклик не найден")

    async def delete(self, id: int):
        for response in self._responses:
            if response.id == id:
                self._responses.remove(response)
                return
        raise ValueError("Отклик не найден")
