from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.application.services.user_service import UserService
from src.presentation.api.dependencies import get_db, get_user_service
from src.presentation.api.schemas.user_schemas import (
    CreateUserRequest,
    UserResponse,
)

from src.application.services.filter_service import FilterService
from src.presentation.api.dependencies import get_filter_service
from src.presentation.api.schemas.filter_schemas import FilterResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
def create_user(
    payload: CreateUserRequest,
    db: Session = Depends(get_db),
):
    service = get_user_service(db)

    try:
        user = service.create_user(
            name=payload.name,
            email=payload.email,
        )
        return user
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
):
    service = get_user_service(db)
    return service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = get_user_service(db)
    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{user_id}/filters", response_model=list[FilterResponse])
def list_user_filters(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = get_filter_service(db)
    return service.list_user_filters(user_id)