from sqlalchemy import ForeignKey, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from datetime import datetime


from storage.sqlalchemy.client import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор вакансии")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), comment="Идентификатор пользователя"
    )
    title: Mapped[str] = mapped_column(String(100), comment="Название вакансии")
    description: Mapped[str] = mapped_column(Text, comment="Описание вакансии")
    salary_from: Mapped[Decimal] = mapped_column(nullable=True, comment="Минимальная зарплата")
    salary_to: Mapped[Decimal] = mapped_column(nullable=True, comment="Максимальная зарплата")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Актуальность вакансии")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, comment="Дата создания")

    user: Mapped["User"] = relationship(back_populates="jobs")  # noqa
    responses: Mapped["Response"] = relationship(back_populates="job")  # noqa
    