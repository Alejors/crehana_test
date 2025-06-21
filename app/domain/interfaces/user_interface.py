from typing import Optional
from abc import ABC, abstractmethod

from app.domain.entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError("Method Not Implemented")
