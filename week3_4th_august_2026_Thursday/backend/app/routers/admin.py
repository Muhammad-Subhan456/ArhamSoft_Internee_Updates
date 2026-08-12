from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.schemas import NoteResponse
from app.services.admin_service import admin_service

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
)


@router.get(
    "/notes",
    response_model=list[NoteResponse],
)
def get_all_notes(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return admin_service.get_all_notes(db)