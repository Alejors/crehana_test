from pydantic import BaseModel, EmailStr

from app.domain.entities import User


class UserBase(BaseModel):
    email: EmailStr
    password: str

    def to_entity(self) -> User:
        return User(email=self.email, password=self.password)


class UserCreate(UserBase):
    username: str

    def to_entity(self) -> User:
        return User(email=self.email, password=self.password, username=self.username)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    @staticmethod
    def from_entity(entity: User) -> "UserOut":
        return UserOut(
            id=entity.id,
            username=entity.username,
            email=entity.email,
        )
