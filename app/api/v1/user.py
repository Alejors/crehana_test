from fastapi import APIRouter, HTTPException, Response, status

from app.usecases import UserUsecase
from app.domain.schemas import UserCreate, UserBase, UserOut, ApiResponse


TOKEN_NAME = "access_token"


def create_user_route(user_usecase: UserUsecase) -> APIRouter:

    router: APIRouter = APIRouter()

    @router.post(
        "/register",
        response_model=ApiResponse[UserOut],
        status_code=status.HTTP_201_CREATED,
    )
    async def register(payload: UserCreate):
        try:
            user_created = await user_usecase.create_user(payload.to_entity())
            return {
                "message": "Registration Successful",
                "data": UserOut.from_entity(user_created),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/login", response_model=ApiResponse[UserOut])
    async def login(payload: UserBase, response: Response):
        try:
            user_exists, token = await user_usecase.login_user(payload.to_entity())
            if not user_exists:
                raise HTTPException(
                    status_code=404, detail="Email and/or Password Incorrect"
                )

            # Seteamos la cookie para que quede disponible en el navegador
            response.set_cookie(
                key=TOKEN_NAME,
                value=token,
                httponly=True,
                secure=False,
                samesite="lax",
            )

            return {
                "message": "Login Successful",
                "data": UserOut.from_entity(user_exists),
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
    async def logout(response: Response):
        response.delete_cookie(key=TOKEN_NAME)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
