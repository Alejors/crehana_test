from pydantic import BaseModel, EmailStr, validator

from app.domain.entities import User


class UserBase(BaseModel):
    email: EmailStr
    password: str

    def to_entity(self) -> User:
        return User(email=self.email, password=self.password)


class UserCreate(UserBase):
    username: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number")
        return value

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
