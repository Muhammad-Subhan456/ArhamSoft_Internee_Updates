from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models import Note, Category, User
from app.schemas import NoteCreate, NoteUpdate


class NoteService:
    
    @staticmethod
    def create_note(
        db: Session,
        note_data: NoteCreate,
        current_user: User,
    ) -> Note:

        if note_data.category_id is not None:
            category = db.scalar(
                select(Category).where(
                    Category.id == note_data.category_id,
                    Category.owner_id == current_user.id,
                )
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

        note = Note(
            title=note_data.title,
            body=note_data.body,
            owner_id=current_user.id,
            category_id=note_data.category_id,
        )

        db.add(note)
        db.commit()

        # Re-fetch so nested owner/category are fresh for the API response.
        return NoteService.get_note(
            db=db,
            note_id=note.id,
            current_user=current_user,
        )

    @staticmethod
    def get_notes(
        db: Session,
        current_user: User,
    ) -> list[Note]:

        return list(
            db.scalars(
                select(Note)
                .options(
                    joinedload(Note.category),
                    joinedload(Note.owner),
                )
                .where(Note.owner_id == current_user.id)
            )
        )

    @staticmethod
    def get_note(
        db: Session,
        note_id: int,
        current_user: User,
    ) -> Note:

        note = db.scalar(
            select(Note)
            .options(
                joinedload(Note.category),
                joinedload(Note.owner),
            )
            .where(
                Note.id == note_id,
                Note.owner_id == current_user.id,
            )
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        return note

    @staticmethod
    def update_note(
        db: Session,
        note_id: int,
        note_data: NoteUpdate,
        current_user: User,
    ) -> Note:

        note = NoteService.get_note(
            db,
            note_id,
            current_user,
        )

        if note_data.category_id is not None:
            category = db.scalar(
                select(Category).where(
                    Category.id == note_data.category_id,
                    Category.owner_id == current_user.id,
                )
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

        note.title = note_data.title
        note.body = note_data.body
        note.category_id = note_data.category_id

        db.commit()

        return NoteService.get_note(
            db=db,
            note_id=note_id,
            current_user=current_user,
        )

    @staticmethod
    def delete_note(
        db: Session,
        note_id: int,
        current_user: User,
    ) -> None:

        note = NoteService.get_note(
            db,
            note_id,
            current_user,
        )

        db.delete(note)
        db.commit()


note_service = NoteService()