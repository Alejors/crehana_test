from app.domain.entities import User
from app.domain.interfaces import IUserRepository
from app.domain.utils import hash_password, verify_password, create_access_token


class UserUsecase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_in: User) -> User:
        # hasheamos el password recibido.
        user_in.password = hash_password(user_in.password)
        return await self.user_repository.create_user(user_in)

    async def login_user(self, user_in: User) -> User:
        user_exist = await self.get_user(user_in.email)
        if not user_exist:
            return None
        if not verify_password(user_in.password, user_exist.password):
            return None

        token = create_access_token({"email": user_exist.email, "id": user_exist.id})
        return user_exist, token

    async def get_user(self, user_email: str) -> User | None:
        return await self.user_repository.get_user_by_email(user_email)
