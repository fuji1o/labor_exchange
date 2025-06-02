from dependency_injector import containers, providers

from interfaces.i_sqlalchemy import ISQLAlchemy
from repositories.job_repository import JobRepository
from repositories.response_repository import ResponseRepository
from repositories.user_repository import UserRepository
from services.job import JobService
from services.response import ResponseService
from services.user import UserService


class RepositoriesContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["web.routers", "dependencies"])

    db = providers.AbstractFactory(ISQLAlchemy)

    user_repository = providers.Factory(
        UserRepository,
        session=db.provided.get_db,
    )

    job_repository = providers.Factory(JobRepository, session=db.provided.get_db)

    response_repository = providers.Factory(ResponseRepository, session=db.provided.get_db)


class ServicesContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["web.routers"])
    repositories_container = providers.DependenciesContainer()

    user_service = providers.Factory(
        UserService,
        user_repository=repositories_container.user_repository,
    )

    job_service = providers.Factory(
        JobService,
        job_repository=repositories_container.job_repository,
        user_repository=repositories_container.user_repository,
    )

    response_service = providers.Factory(
        ResponseService,
        response_repository=repositories_container.response_repository,
        job_repository=repositories_container.job_repository,
        user_repository=repositories_container.user_repository,
    )
