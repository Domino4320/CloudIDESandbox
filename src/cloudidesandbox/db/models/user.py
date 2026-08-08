from src.cloudidesandbox.db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
