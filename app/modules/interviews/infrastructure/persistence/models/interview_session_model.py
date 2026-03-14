from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class InterviewSessionModel(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
