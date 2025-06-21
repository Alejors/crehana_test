from typing import List
from fastapi import APIRouter, HTTPException, status, Request

from app.usecases import UserUsecase
from app.domain.schemas import UserCreate, UserBase, UserOut, ApiResponse


def create_user_route(user_usecase: UserUsecase) -> APIRouter:

    router: APIRouter = APIRouter()
    
    @router.post("/register", response_model=ApiResponse[UserOut])
    async def register(payload: UserCreate):
        try:
            user_created = await user_usecase.create_user(payload.to_entity())
            return {"message": "Registration Successful", "data": UserOut.from_entity(user_created)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    @router.post("/login", response_model=ApiResponse[UserOut])
    async def login(payload: UserBase):
        try:
            user_exists = await user_usecase.login_user(payload.to_entity())
            if not user_exists:
                raise HTTPException(status_code=404, detail="Email and/or Password Incorrect")
            return {"message": "Login Successful", "data": UserOut.from_entity(user_exists)}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    return router