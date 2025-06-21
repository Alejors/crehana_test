from sqlalchemy import select
from typing import Optional
from sqlalchemy.orm import Session

from app.domain.entities import User
from app.domain.interfaces import IUserRepository
from app.infrastructure.db.models.user import UserModel


class SQLAlchemyUserRepository(IUserRepository):
    
    def __init__(
        self,
        session: Session,
    ):
        self.db = session      

    async def _find_by_email(self, session, email: str):
        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.deleted_at.is_(None),
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.db() as session:
            user_model = await self._find_by_email(session, email)
            return user_model.to_entity() if user_model else None
    
    async def create_user(self, user_in: User) -> User:
        async with self.db() as session:
            user_model = UserModel.from_entity(user_in)
            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)
            return user_model.to_entity()
