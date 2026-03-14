from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class DepartmentModel(Base):
    __tablename__ = "departments"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
