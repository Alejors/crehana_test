from sqlalchemy import Column, Integer, String
from app.infrastructure.db import Base
from .timemixin import TimestampMixin

from app.domain.entities import User


class UserModel(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    @staticmethod
    def from_entity(entity: User) -> "UserModel":
        return UserModel(
            id=entity.id if entity.id else None,
            username=entity.username,
            email=entity.email,
            password=entity.password,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
