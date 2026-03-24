from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.presentation.api.dependencies import get_db, get_filter_service
from src.presentation.api.schemas.filter_schemas import (
    CreateFilterRequest,
    FilterResponse,
)

from src.presentation.api.dependencies import get_listing_monitor_service
router = APIRouter(prefix="/filters", tags=["filters"])


@router.post("", response_model=FilterResponse)
def create_filter(
    payload: CreateFilterRequest,
    db: Session = Depends(get_db),
):
    service = get_filter_service(db)

    try:
        search_filter = service.create_filter(
            user_id=payload.user_id,
            name=payload.name,
            olx_url=payload.olx_url,
            check_interval_minutes=payload.check_interval_minutes,
        )
        return search_filter
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{filter_id}/activate", response_model=FilterResponse)
def activate_filter(
    filter_id: int,
    db: Session = Depends(get_db),
):
    service = get_filter_service(db)

    try:
        return service.activate_filter(filter_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/{filter_id}/deactivate", response_model=FilterResponse)
def deactivate_filter(
    filter_id: int,
    db: Session = Depends(get_db),
):
    service = get_filter_service(db)

    try:
        return service.deactivate_filter(filter_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.post("/{filter_id}/run")
def run_filter(
    filter_id: int,
    db: Session = Depends(get_db),
):
    service = get_listing_monitor_service(db)

    try:
        new_matches = service.run_filter_check(filter_id)
        return {
            "filter_id": filter_id,
            "new_matches": new_matches,
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))