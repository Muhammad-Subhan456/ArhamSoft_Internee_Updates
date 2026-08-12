from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Note


class AdminService:

    @staticmethod
    def get_all_notes(db: Session):

        return list(
            db.scalars(
                select(Note)
                .options(
                    joinedload(Note.owner),
                    joinedload(Note.category),
                )
            )
        )


admin_service = AdminService()