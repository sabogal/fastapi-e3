# app/interfaces/api/user_api.py
from fastapi import APIRouter, Depends, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.microservices.users.application.use_cases.user_use_case import UserUseCase
from app.microservices.users.infrastructure.repositories.user_repository import UserRepository
from app.microservices.users.infrastructure.database.db_postgrest import get_db
from app.microservices.users.interface.mappers.user_mapper import UserMapper
from app.microservices.users.domain.exceptions.user_exception import CustomExcepcion
from ..schemas.user_schema import UserCreateSchema, UserUpdateSchema

router = APIRouter()


@router.post("/users/")
def create(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        use_case = UserUseCase(UserRepository(db))
        new_user = use_case.create(UserMapper.schema_to_dto(user))
        return new_user
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )
        
@router.patch("/users/{pk}")
def update(
    user: UserUpdateSchema,
    pk: int = Path(..., description="ID del usuario"),
    db: Session = Depends(get_db)
):
    try:
        use_case = UserUseCase(UserRepository(db))
        new_user = use_case.update(pk, UserMapper.schema_to_dto(user, partial=True))
        return new_user
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )

@router.get("/users/")
def get_all(db: Session = Depends(get_db)):
    use_case = UserUseCase(UserRepository(db))
    users = use_case.get_all()
    return users


@router.get("/users/{pk}")
def get_by_id(pk: int = Path(..., description="ID del usuario"), db: Session = Depends(get_db)):
    try:
        use_case = UserUseCase(UserRepository(db))
        user = use_case.get_by_id(pk)
        return user
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )

@router.delete("/users/{pk}")
def delete(pk: int = Path(..., description="ID del usuario"), db: Session = Depends(get_db)):
    try:
        use_case = UserUseCase(UserRepository(db))
        use_case.delete(pk)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'detail': 'Usuario eliminado con éxito.'}
        )
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )
