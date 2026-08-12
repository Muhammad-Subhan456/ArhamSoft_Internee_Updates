from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.services.note_service import note_service

router = APIRouter(
    prefix="/api/v1/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.create_note(
        db=db,
        note_data=note,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[NoteResponse],
)
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.get_notes(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.get_note(
        db=db,
        note_id=note_id,
        current_user=current_user,
    )


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.update_note(
        db=db,
        note_id=note_id,
        note_data=note,
        current_user=current_user,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note_service.delete_note(
        db=db,
        note_id=note_id,
        current_user=current_user,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)